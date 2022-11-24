# coding=utf-8
#########################################################################
# File Name: front.py
# Author: Haoyang Meng
# mail: 905505155@qq.com
# Created Time: 11/23/2022 9:06:13
# Description:
########################################################################
import tkinter as tk
from tkinter import filedialog
import os
def list_click(event):
    print('列表框组件的内容被点击了')
    index = list_box.curselection()[0]
    path = list_box.get(index)
    print(path)
    content = open(path, mode='r', encoding='utf-8').read()
    print(content)
    top = tk.Toplevel(root)
    filename = path.split('/')[-1]
    top.title(filename)
    text = tk.Text(top)
    text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    text.insert(tk.END, content)


def search():
    print('按钮被点击了')

root = tk.Tk()
root.geometry('800x500')
root.title('浏览器记录搜索工具')


search_frame = tk.Frame(root)
search_frame.pack()
tk.Label(search_frame, text='关键字:').pack(side=tk.LEFT, padx=10, pady=10)
key_entry = tk.Entry(search_frame)  # 创建一个输入框
key_entry.pack(side=tk.LEFT, padx=10, pady=10)  # 将输入框显示到界面
tk.Label(search_frame, text='文件类型:').pack(side=tk.LEFT, padx=10, pady=10)
type_entry = tk.Entry(search_frame)
type_entry.pack(side=tk.LEFT, padx=10, pady=10)
button = tk.Button(search_frame, text='搜索')
button.pack(side=tk.LEFT, padx=10, pady=10)
##添加边框
list_box = tk.Listbox(root)
list_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


button.config(command=search)

key = key_entry.get()
file_type = type_entry.get()
print(key, file_type)

dir_path = filedialog.askdirectory()
print(dir_path)  # 遍历文件，实现搜索功能
file_list = os.walk(dir_path)

for root_path, dirs, files in file_list:
    # 目录路径，目录下的子目录，目录下的文件
    # print(root_path, dirs, files)
    for file in files:
        # 过滤文件类型，搜索关键字
        if type_entry:  # py 如果输入了类型，就进行过滤，如果没有输入，就不过滤类型
            if file.endswith(file_type):
                # 搜索关键字
                content = open(root_path + '/' + file, mode='r', encoding='utf-8-sig').read()

                if key in content:
                    print(root_path + '/' + file)
                    # 把结果显示到界面上
                    list_box.insert(tk.END, root_path + '/' + file)

sb = tk.Scrollbar(root)
sb.pack(side=tk.RIGHT, fill=tk.Y)
sb.config(command=list_box.yview)
list_box.config(yscrollcommand=sb.set)
list_box.bind('<Double-Button-1>', list_click)



root.mainloop()
