# coding=utf-8
#########################################################################
# File Name: front.py
# Author: Haoyang Meng
# E-mail: 905505155@qq.com
# Created Time: 11/23/2022 9:06:13
# Description:
########################################################################

import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL.ImageTk import PhotoImage
import main_server

# 后端配合
path_name = ''
browser_version = ''
custom_keyword_place = ''

##实现调用窗口内的各个子元件
def windows_front_main():
    windows = tk.Tk()
    windows.geometry('520x220')
    windows_title(windows)
    select(windows)
    windows.mainloop()

def windows_title(windows):
    windows.title('Browser Record Prasing')
    # title_img = PhotoImage(file="favicon.ico")
    ##需要pillow库
    # windows.tk.call('wm', 'iconphoto', windows._w, title_img)

##实现下拉选择栏，选择浏览器的版本
def select(windows):

    select_frame = tk.Frame(windows)
    select_frame.pack(expand=False, fill="both", padx=10, pady=10)
    path_frame = tk.Frame(windows)
    path_frame.pack(expand=False, fill="both", padx=10, pady=10)
    click_frame = tk.Frame(windows)
    click_frame.pack(expand=False, fill="both", padx=10, pady=10)

    tk.Label(select_frame, text='Select Browser Version:').pack(side='left')
    ##储存列表
    select_data = ("Firefox", "Chromium")  # 使用元组
    var = tk.StringVar(select_frame)
    var.set("- Select -")
    optionmenu = tk.OptionMenu(select_frame, var, *select_data)
    optionmenu.pack(side=tk.LEFT)

    def selectPath_dir():
        path_ = filedialog.askdirectory()
        var_path.set(path_)
    tk.Label(path_frame, text="Select the Path:").pack(side='left')
    var_path = tk.StringVar()  # 文件夹输入路径变量
    var_path.set("Input or select Browser Profile Path")
    entry_name = tk.Entry(path_frame, textvariable=var_path, width=55)
    entry_name.pack(side='left')
    tk.Button(path_frame, text='Select', command=selectPath_dir).pack(side='right')

    var_file = tk.StringVar()  # 文件输入路径变量
    var_file.set("None")
    entry_file = tk.Entry(click_frame, textvariable=var_file, width=55,state=tk.DISABLED)
    entry_file.pack(side='left')

    def selectPath_file():
        path_ = filedialog.askopenfilename(filetypes=[("Key word", [".txt"])])
        var_file.set(path_)
    click_button = tk.Checkbutton(click_frame, text='Custom Keyword', command=selectPath_file)
    click_button.pack(side='right')

    start_button(windows, var, var_path, var_file)

##开始程序的按钮
def start_button(windows,var,var_path,var_file):
    def printSelection():
        print("The selection is : ", var.get(),"The Path is : ",var_path.get(),"The File is:",var_file.get())
        browser_version = str(var.get())
        path_name = var_path.get()
        custom_keyword_place = var_file.get()
        main_server.main(path_name = path_name, browser_version = browser_version, custom_keyword_place = custom_keyword_place)
    start_frame = tk.Frame(windows)
    start_frame.pack()
    button = tk.Button(start_frame, text='Start Parsing', bg='white',command=printSelection)
    button.pack(side=tk.BOTTOM, padx=20, pady=20)


##实现展示输出结果的窗口
def list_windows(output_windows):
    start_frame = tk.Frame(output_windows)
    start_frame.pack()


if __name__ == '__main__':
    windows_front_main()

