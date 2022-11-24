import main_server
from tkinter import filedialog

path_name = filedialog.askdirectory()
main_server.main(path_name = path_name, browser_version = 'Firefox', custom_keyword_place = '')
