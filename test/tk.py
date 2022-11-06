from tkinter import *
from tkinter.filedialog import askdirectory
import os

profile_path = ''

def selectPath():
    path_ = askdirectory() #使用askdirectory()方法返回文件夹的路径
    if path_ == "":
        path.get() #当打开文件路径选择框后点击"取消" 输入框会清空路径，所以使用get()方法再获取一次路径
    else:
        profile_path_ = path_.replace("/", "\\")  # 实际在代码中执行的路径为“\“ 所以替换一下
        # path.set(path_)
        


def openPath():
    dir = os.path.dirname(path.get()+"\\")
    os.system('start ' + dir)
    #print(dir)

def window():
    root = Tk()
    root.title("Browser Record Exporting")
    path = StringVar()
    path.set(os.path.expanduser('~'))
    # path.set(os.path.abspath("~"))

    Label(root, text="Browser Profile Location:").grid(row=0, column=0)
    Entry(root, textvariable=path,state="readonly").grid(row=0, column=1,ipadx=200)

    # e.insert(0,os.path.abspath("."))
    Button(root, text="Path", command=selectPath).grid(row=0, column=2)
    Button(root, text="Open File Location", command=openPath).grid(row=0, column=3)
    root.mainloop()

if __name__ == '__main__':
    window()