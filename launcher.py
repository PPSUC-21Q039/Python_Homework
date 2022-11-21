# coding=utf-8
#########################################################################
# File Name: main.py
# Author: Wenqiang Hu
# mail: huwenqiang.hwq@protonmail.com
# Created Time: 11/5/2022 10:57:13
# Description: See Readme.md
########################################################################


import re
import os
import json
import sqlite3
import optparse
import urllib.parse  # Decode the URL Code
from datetime import datetime, timedelta

# Change the Default Encoding
import io
import sys


# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding = 'utf8')
OUTPUT_FILE = "./output.txt"
OUTPUT = open (OUTPUT_FILE, "w")

# Parsing Firefox-based browsers, such as Mozilla Firefox (including mutiple detailed versions like ESR and Nightly), Tor Browser and so on.
class Firefox:
    # Parsing the file downloads.sqlite and output the download record
    def print_downloads(download_db):
        conn = sqlite3.connect(download_db)
        c = conn.cursor()
        c.execute('SELECT name, source, datetime(endTime/1000000, \'unixepoch\') FROM moz_downloads;')
        print('\n[*] -- Files Downloaded -- ', file = OUTPUT)
        for row in c:
            print('[+] File: ' + str(row[0]) + ' from source: ' + str(row[1]) + ' at: ' + str(row[2]), file = OUTPUT)
        return

        # Parsing the file cookies.sqlite and output the Cookies

    def print_cookies(cookies_db):
        try:
            conn = sqlite3.connect(cookies_db)
            c = conn.cursor()
            c.execute('SELECT host, name, value FROM moz_cookies')

            print('\n[*] -- Cookies --', file = OUTPUT)
            for row in c:
                host = str(row[0])
                name = str(row[1])
                value = str(row[2])
                # print('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value)
                # Common Sites
                if 'google' in host.lower():
                    print('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value, file = OUTPUT)
                if 'baidu' in host.lower():
                    print('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value, file = OUTPUT)
                if 'bing' in host.lower():
                    print('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value, file = OUTPUT)
                if 'youtube' in host.lower():
                    print('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value, file = OUTPUT)
                if 'facebook' in host.lower():
                    print('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value, file = OUTPUT)
                if 'instagram' in host.lower():
                    print('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value, file = OUTPUT)
                if 'twitter' in host.lower():
                    print('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value, file = OUTPUT)
                if 'tx' in host.lower():
                    print('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value, file = OUTPUT)
                if 'sogou' in host.lower():
                    print('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value, file = OUTPUT)
                if 'vpn' in host.lower():
                    print('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value, file = OUTPUT)

        except Exception as e:
            if 'encrypted' in str(e):
                print('\n[*] Error reading your cookies database.')
                print('[*] Upgrade your Python-Sqlite3 Library')
                print('\n[*] Error reading your cookies database.', file = OUTPUT)
                print('[*] Upgrade your Python-Sqlite3 Library', file = OUTPUT)
        return

    # Parsing the file places.sqlite and output the History Record
    def print_history(places_db):
        try:
            conn = sqlite3.connect(places_db)
            c = conn.cursor()
            c.execute("select url, datetime(visit_date/1000000, 'unixepoch') from moz_places, moz_historyvisits \
                    where visit_count > 0 and moz_places.id==moz_historyvisits.place_id;")

            print('\n[*] -- Browsing History --', file = OUTPUT)
            for row in c:
                url = str(row[0])
                date = str(row[1])
                print('[+] ' + date + ' - Visited: ' + url, file = OUTPUT)
        except Exception as e:
            if 'encrypted' in str(e):
                print('\n[*] Error reading your places database.')
                print('[*] Upgrade your Python-Sqlite3 Library')
                print('\n[*] Error reading your places database.', file = OUTPUT)
                print('[*] Upgrade your Python-Sqlite3 Library', file = OUTPUT)
                sys.exit(0)
        print("\n", file = OUTPUT)
        return

        # Parsing the file placed.sqlite and output the Search History

    def print_search_engine(places_db):
        try:
            conn = sqlite3.connect(places_db)
            c = conn.cursor()
            c.execute("select url, datetime(visit_date/1000000, 'unixepoch') from moz_places, moz_historyvisits \
                    where visit_count > 0 and moz_places.id==moz_historyvisits.place_id;")
        except Exception as e:
            if 'encrypted' in str(e):
                print('\n[*] Error reading your cookies database.')
                print('[*] Upgrade your Python-Sqlite3 Library')
                print('\n[*] Error reading your cookies database.', file = OUTPUT)
                print('[*] Upgrade your Python-Sqlite3 Library', file = OUTPUT)
                sys.exit(0)

        print('\n[*] -- Search Engine History --', file = OUTPUT)
        # Baidu
        for row in c:
            url = str(row[0])
            date = str(row[1])
            if 'baidu' in url.lower():
                r = re.findall(r'wd=.*?\&', url)
                if r:
                    search = r[0].split('&')[0]
                    search = search.replace('wd=', '').replace('+', ' ')
                    search = urllib.parse.unquote(search)
                    print('[+] ' + date + ' - Searched Baidu For: ' + search, file = OUTPUT)
        # Bing
        for row in c:
            url = str(row[0])
            date = str(row[1])
            if 'bing' in url.lower():
                r = re.findall(r'q=.*\&', url)
                if r:
                    search = r[0].split('&')[0]
                    search = search.replace('q=', '').replace('+', ' ')
                    print('[+] ' + date + ' - Searched Bing For: ' + search, file = OUTPUT)

        # Google
        for row in c:
            url = str(row[0])
            date = str(row[1])
            if 'google' in url.lower():
                r = re.findall(r'q=.*\&', url)
                if r:
                    print(r)
                    search = r[0].split('&')[0]
                    search = search.replace('q=', '').replace('+', ' ')
                    print('[+] ' + date + ' - Searched Google For: ' + search, file = OUTPUT)

        # Duckduckgo
        for row in c:
            url = str(row[0])
            date = str(row[1])
            if 'duckduckgo' in url.lower():
                r = re.findall(r'q=.*\&', url)
                if r:
                    search = r[0].split('&')[0]
                    search = search.replace('q=', '').replace('+', ' ')
                    print('[+] ' + date + ' - Searched Duckduckgo For: ' + search, file = OUTPUT)

        # Yandex
        for row in c:
            url = str(row[0])
            date = str(row[1])
            if 'yandex' in url.lower():
                r = re.findall(r'text=.*\&', url)
                if r:
                    search = r[0].split('&')[0]
                    search = search.replace('text=', '').replace('+', ' ')
                    print('[+] ' + date + ' - Searched Yandex For: ' + search, file = OUTPUT)

        # Startpage
        for row in c:
            url = str(row[0])
            date = str(row[1])
            if 'startpage' in url.lower():
                r = re.findall(r'q=.*\&', url)
                if r:
                    search = r[0].split('&')[0]
                    search = search.replace('q=', '').replace('+', ' ')
                    print('[+] ' + date + ' - Searched Startpage For: ' + search, file = OUTPUT)

        # Sougou
        for row in c:
            url = str(row[0])
            date = str(row[1])
            if 'sogou' in url.lower():
                r = re.findall(r'query=.*\&', url)
                if r:
                    search = r[0].split('&')[0]
                    search = search.replace('query=', '').replace('+', ' ')
                    print('[+] ' + date + ' - Searched For: ' + search, file = OUTPUT)

        # WikiPedia
        for row in c:
            url = str(row[0])
            date = str(row[1])
            if 'wikipedia' in url.lower():
                r = re.findall(r'wd=.*\&', url)
                if r:
                    search = r[0].split('&')[0]
                    search = search.replace('wd=', '').replace('+', ' ')
                    print('[+] ' + date + ' - Searched For: ' + search, file = OUTPUT)

        print("\n", file = OUTPUT)
        return

    # Parsing the file places.sqlite and output the Bookmark Names and URLs
    def print_bookmark(places_db):
        try:
            conn = sqlite3.connect(places_db)
            c = conn.cursor()
        except Exception as e:
            if 'encrypted' in str(e):
                print('\n[*] Error reading your cookies database.')
                print('[*] Upgrade your Python-Sqlite3 Library')
                print('\n[*] Error reading your cookies database.', file = OUTPUT)
                print('[*] Upgrade your Python-Sqlite3 Library', file = OUTPUT)
                sys.exit(0)

        print('\n[*] --- Bookmarks --- ', file = OUTPUT)
        url_sql = c.execute("select * from moz_places")
        for url_row in url_sql:
            url = str(url_row[1])
            print('[+] ', url, sep = '', file = OUTPUT)
        

# Parsing Chromium-based browsers, such as Chromium, Google Chrome, Edge, 360 Series and so on.
class Chromium:
    def get_chrome_datetime(chromedate):
        return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

    def print_bookmark(bookmark_file):
        try:
            with open(bookmark_file, 'r', encoding='utf-8') as input_bookmark:
                bookmark_content = input_bookmark.read()
                bookmark_json = json.loads(bookmark_content)
        except:
            print("[*] Error reading bookmark file: " + bookmark_file, file = OUTPUT)
            return
        print("[*] -- Bookmarks --", file = OUTPUT)
        for bookmark in bookmark_json["roots"]["bookmark_bar"]["children"]:
            print(bookmark["name"] + ': ' + bookmark["url"], file = OUTPUT)
        return

    def print_history(history_db):
        conn = sqlite3.connect(history_db)
        c = conn.cursor()
        c.execute("SELECT id,url,title,visit_count,last_visit_time  from urls")
        print('\n\n\n[*] -- Browsing History --', file = OUTPUT)
        for _id, url, title, visit_count, last_visit_time in c:
            time = str(Chromium.get_chrome_datetime(last_visit_time))
            print('[+] ' + time + ' Visited ' + title + ': ' + url, file = OUTPUT)
        return

    def print_search_engine(history_db):
        conn = sqlite3.connect(history_db)
        c = conn.cursor()
        c.execute("SELECT normalized_term FROM keyword_search_terms;")
        print('\n\n\n[*] -- Search Engine Record -- ', file = OUTPUT)
        for row in c:
            print('[+] Search Record: ' + str(row), file = OUTPUT)
        return

    def print_downloads(download_db):
        conn = sqlite3.connect(download_db)
        c = conn.cursor()
        c.execute("SELECT url FROM downloads_url_chains;")
        print('\n\n\n[*] -- Files Downloaded -- ', file = OUTPUT)
        for row in c:
            print('[+] File: ' + str(row), file = OUTPUT)
        return

    def customized_print_bookmark(bookmark_file, customized_keyword):
        try:
            with open(bookmark_file, 'r', encoding='utf-8') as input_bookmark:
                bookmark_content = input_bookmark.read()
                bookmark_json = json.loads(bookmark_content)
        except:
            print("[*] Error reading bookmark file: " + bookmark_file, file = OUTPUT)
            return

        print("\n\n[*] -- Bookmarks that hint customized keywords --", file = OUTPUT)
        for bookmark in bookmark_json["roots"]["bookmark_bar"]["children"]:
            for keyword in customized_keyword:
                if keyword.lower() in bookmark["name"].lower() or keyword.lower() in bookmark["url"].lower():
                    print('[+] Bookmark hint keyword \"' + keyword.strip() + '\": ' + bookmark["name"] + ' ' + bookmark[
                        "url"], file = OUTPUT)
        return

    def customized_print_history(history_db, customized_keyword):
        conn = sqlite3.connect(history_db)
        c = conn.cursor()
        c.execute("SELECT id,url,title,visit_count,last_visit_time  from urls")
        print('\n\n\n[*] -- Browsing History that contain customized keyword --', file = OUTPUT)
        for _id, url, title, visit_count, last_visit_time in c:
            time = str(Chromium.get_chrome_datetime(last_visit_time))
            for keyword in customized_keyword:
                if keyword.lower() in title.lower() or keyword.lower() in url.lower():
                    print('[+] ' + time + ' Visite History hint keyword \"' + keyword.strip() + '\": ' + title + ', ' + url, file = OUTPUT)
        return

    def customized_print_search_engine(history_db, customized_keyword):
        conn = sqlite3.connect(history_db)
        c = conn.cursor()
        c.execute("SELECT normalized_term FROM keyword_search_terms;")
        print('\n[*] -- Search engine record that hint customized keywords -- ', file = OUTPUT)
        for row in c:
            for keyword in customized_keyword:
                if keyword.lower() in row[0].lower():
                    print('[+] Search Record hint keyword \"' + keyword + '\": ' + str(row), file = OUTPUT)
        return

    def customized_print_downloads(download_db, customized_keyword):
        conn = sqlite3.connect(download_db)
        c = conn.cursor()
        c.execute("SELECT url FROM downloads_url_chains;")
        print('\n\n[*] -- Files Downloaded that hint customized keywords -- ', file = OUTPUT)
        for row in c:
            for keyword in customized_keyword:
                if keyword.lower() in row[0].lower():
                    print('[+] File hint keyword \"' + keyword + '\": ' + str(row), file = OUTPUT)
        return


def main():
    USER_DIRECTORY = os.path.expanduser('~')
    FIREFOX_PROFILE_DIRECTORY = os.path.join(USER_DIRECTORY, "AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\")
    CHROMIUM_PROFILE_DIRECTORY = ""

    print("Choose a browser series: \n1. Firefox\n2. Chromium")
    browser_choice = int(input())
    if browser_choice == 1:
        # Firefox
        profiles = os.listdir(FIREFOX_PROFILE_DIRECTORY)
        serial_number = 1
        print("Profile found under: ", FIREFOX_PROFILE_DIRECTORY, sep = '')
        print("Profile found under: ", FIREFOX_PROFILE_DIRECTORY, sep = '', file = OUTPUT)
        print("Please enter the serial of the profile: ")
        print("Please enter the serial of the profile: ", file = OUTPUT)
        for profile in profiles:

            print(serial_number, ": ", profile, sep = '')
            print(serial_number, ": ", profile, sep = '', file = OUTPUT)
            serial_number = serial_number + 1

        profile_choice = int(input())
        profile_choice = profile_choice - 1
        profile = profiles[profile_choice]
        profile_addr = os.path.join(FIREFOX_PROFILE_DIRECTORY, profile)
        path_name = profile_addr

        if os.path.isdir(path_name) == False:
            print('[!] Path Does Not Exist: ' + path_name)
            print('[!] Path Does Not Exist: ' + path_name, file = OUTPUT)
            raise Exception("PathNotExist")
            sys.exit(0)
        else:
            download_db = os.path.join(path_name, 'downloads.sqlite')
            if os.path.isfile(download_db):
                Firefox.print_downloads(download_db)
            else:
                print('[!] Downloads Db (downloads.sqlite) does not exist: ' + download_db)
                print('[!] Downloads Db (downloads.sqlite) does not exist: ' + download_db, file = OUTPUT)

            # cookies.sqlite
            cookies_db = os.path.join(path_name, 'cookies.sqlite')
            if os.path.isfile(cookies_db):
                Firefox.print_cookies(cookies_db)
            else:
                print('[!] Cookies Db (cookies.sqlite) does not exist:' + cookies_db)
                print('[!] Cookies Db (cookies.sqlite) does not exist:' + cookies_db, file = OUTPUT)

            # places.sqlite
            places_db = os.path.join(path_name, 'places.sqlite')
            if os.path.isfile(places_db):
                Firefox.print_history(places_db)
                Firefox.print_search_engine(places_db)
                Firefox.print_bookmark(places_db)
            else:
                print('[!] places_db (places.db) does not exist: ' + places_db)
                print('[!] places_db (places.db) does not exist: ' + places_db, file = OUTPUT)

        print("[*] Firefox Analyzing Completed! ")
    elif browser_choice == 2:
        pass
    else:
        print("Error!")
    return


if __name__ == '__main__':
    main()
