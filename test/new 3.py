import os
import sqlite3
import json
import win32crypt
import shutil
import base64
from Crypto.Cipher import AES
from datetime import datetime, timedelta
import pandas as pd
import traceback

# chrome data path
hostname = os.getlogin()
CHROME_PATH = f"C:/Users/{hostname}/AppData/Local/Google/Chrome/User Data/Default"
EDGE_PATH = f"C:/Users/{hostname}/AppData/Local/Microsoft/Edge/User Data/Default"
EDGE_KILL = "taskkill /f /t /im msedge.exe"
CHROME_KILL = "taskkill /f /t /im chrome.exe"


def get_chrome_datetime(chromedate):
    """
    从chrome格式的datetime返回一个`datetime.datetime`对象
    因为'chromedate'的格式是1601年1月以来的微秒数
    """
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)


# chrome browser bookmark
class BookMark:

    def __init__(self, chromePath=CHROME_PATH):
        # chromepath
        self.chromePath = chromePath
        self.browse_type = chromePath.split("/")[6]
        # refresh bookmarks
        self.bookmarks = self.get_bookmarks()

    def get_folder_data(self, folder=0):
        """获取收藏夹所有的文件夹内容，合并后保存"""
        df = []
        for mark_name, item in self.bookmarks["roots"].items():
            try:
                data = pd.DataFrame(item["children"])
                data["folder_name"] = item["name"]
                df.append(data)
            except Exception:
                traceback.print_exc()
                print(mark_name)
        pd.concat(df).to_csv("results_%s.csv"%self.browse_type, encoding="gbk")

    def get_bookmarks(self):
        'update chrome data from chrome path'
        # parse bookmarks
        assert os.path.exists(
            os.path.join(self.chromePath,
                         'Bookmarks')), "can't found ‘Bookmarks’ file,or path isn't a chrome browser cache path!"
        with open(os.path.join(self.chromePath, 'Bookmarks'), encoding='utf-8') as f:
            return json.loads(f.read())


# History
class History:
    def __init__(self, kill_exe, chromePath=CHROME_PATH, ):
        os.system(kill_exe)
        self.chromePath = chromePath
        self.browse_type = chromePath.split("/")[6]
        self.connect()

    def connect(self):
        assert os.path.exists(
            os.path.join(self.chromePath,
                         'History')), "can't found ‘History’ file,or path isn't a chrome browser cache path!"
        self.conn = sqlite3.connect(os.path.join(self.chromePath, "History"))
        self.cousor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def set_chrome_path(self, chromePath):
        self.close()
        self.chromePath = chromePath
        self.connect()

    def get_history(self):
        cursor = self.conn.execute("SELECT id,url,title,visit_count,last_visit_time  from urls")
        rows = []
        for _id, url, title, visit_count, last_visit_time in cursor:
            row = {}
            row['id'] = _id
            row['url'] = url
            row['title'] = title
            row['visit_count'] = visit_count
            row['last_visit_time'] = get_chrome_datetime(last_visit_time)
            rows.append(row)
        pd.DataFrame(rows).to_csv("browse_history_%s.csv"%self.browse_type, encoding="utf-8")
        return rows

    def get_downloads(self):
        cursor = self.conn.execute("SELECT start_time,target_path,tab_url from downloads")
        rows = []
        for start_time, target_path, tab_url in cursor:
            row = {}
            row['start_time'] = start_time
            row['tab_url'] = tab_url
            row['target_path'] = target_path
            rows.append(row)
        pd.DataFrame(rows).to_csv("download_history_%s.csv"%self.browse_type, encoding="utf-8")
        return rows


class Password:
    def __init__(self, kill_exe, path=EDGE_PATH):
        """
        self.path: User Data的路径
        """
        os.system(kill_exe)
        self.path = path
        self.browse_type = path.split("/")[6]
    def get_encryption_key(self):
        local_state_path = os.path.join(os.path.split(self.path)[0], "Local State")
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        key = key[5:]
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

    def decrypt_password(self, password, key):
        try:
            iv = password[3:15]
            password = password[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            return cipher.decrypt(password)[:-16].decode()
        except:
            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                import traceback
                traceback.print_exc()
                return ""

    def parse_password(self):
        key = self.get_encryption_key()
        db_path = os.path.join(EDGE_PATH, "Login Data")
        # 复制一份数据库文件出来
        filename = "ChromeData.db"
        shutil.copyfile(db_path, filename)
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        cursor.execute(
            "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
        rows = []
        for row in cursor.fetchall():
            origin_url = row[0]
            action_url = row[1]
            username = row[2]
            password = self.decrypt_password(row[3], key)
            date_created = row[4]
            date_last_used = row[5]
            item = {}
            if username or password:
                item["origin_url"] = origin_url
                item["action_url"] = action_url
                item["username"] = username
                item["password"] = password
            if date_created != 86400000000 and date_created:
                item["creation_date"] = str(get_chrome_datetime(date_created))
            if date_last_used != 86400000000 and date_last_used:
                item["last_used"] = str(get_chrome_datetime(date_last_used))
            rows.append(item)

        cursor.close()
        db.close()
        try:
            # try to remove the copied db file
            os.remove(filename)
            pd.DataFrame(rows).to_csv("passwords_%s.csv"%self.browse_type)
        except:
            import traceback
            traceback.print_exc()

def main():
    
    for kill_cmd,path in zip([EDGE_KILL],[EDGE_PATH]):
        if os.path.exists(path):
            # 获取收藏夹数据
            try:
                BookMark(path).get_folder_data()
                # 获取历史记录
                History(kill_cmd, path).get_history()
                History(kill_cmd, path).get_downloads()
                # 获取密码
                Password(kill_cmd, path).parse_password()
            except Exception as e:
                traceback.print_exc()
if __name__ == '__main__':
    main()
