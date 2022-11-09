# coding=utf-8
#########################################################################
# File Name: main.py
# Author: Wenqiang Hu
# mail: huwenqiang.hwq@protonmail.com
# Created Time: 11/5/2022 10:57:13
# Requirements:
#   python -m pip install optparse
########################################################################


import re
import os
import json
import time
import sqlite3
import optparse
import urllib.parse  # Decode the URL Code
from datetime import datetime, timedelta

# Change the Default Encoding 
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')


# Parsing Firefox-based browsers, such as Mozilla Firefox (including mutiple detailed versions like ESR and Nightly), Tor Browser and so on.
class Firefox:
    # Parsing the file downloads.sqlite and output the download record
    def print_downloads(download_db):
        conn = sqlite3.connect(download_db)
        c = conn.cursor()
        c.execute('SELECT name, source, datetime(endTime/1000000, \'unixepoch\') FROM moz_downloads;')
        print('\n[*] -- Files Downloaded -- ')
        for row in c:
            print('[+] File: ' + str(row[0]) + ' from source: ' + str(row[1]) + ' at: ' + str(row[2]))
        return 


    # Parsing the file cookies.sqlite and output the Cookies
    def print_cookies(cookies_db):
        try:
            conn = sqlite3.connect(cookies_db)
            c = conn.cursor()
            c.execute('SELECT host, name, value FROM moz_cookies')

            print('\n[*] -- Cookies --')
            for row in c:
                host = str(row[0])
                name = str(row[1])
                value = str(row[2])
                # print('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value)
                # Common Sites
                if 'google' in host.lower():
                    print('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value)
                if 'baidu' in host.lower():
                    print('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value)
                if 'bing' in host.lower():
                    print('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value)
                if 'youtube' in host.lower():
                    print('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value)
                if 'facebook' in host.lower():
                    print('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value)
                if 'instagram' in host.lower():
                    print('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value)
                if 'twitter' in host.lower():
                    print('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value)
                if 'tx' in host.lower():
                    print('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value)
                if 'sogou' in host.lower():
                    print('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value)
                if 'vpn' in host.lower():
                    print('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value)

        except Exception(e):
            if 'encrypted' in str(e):
                print('\n[*] Error reading your cookies database.')
                print('[*] Upgrade your Python-Sqlite3 Library')
        return


    # Parsing the file places.sqlite and output the History Record
    def print_history(places_db):
        try:
            conn = sqlite3.connect(places_db)
            c = conn.cursor()
            c.execute("select url, datetime(visit_date/1000000, 'unixepoch') from moz_places, moz_historyvisits \
                    where visit_count > 0 and moz_places.id==moz_historyvisits.place_id;")

            print('\n[*] -- Browsing History --')
            for row in c:
                url = str(row[0])
                date = str(row[1])
                print('[+] ' + date + ' - Visited: ' + url)
        except Exception(e):
            if 'encrypted' in str(e):
                print('\n[*] Error reading your places database.')
                print('[*] Upgrade your Python-Sqlite3 Library')
                sys.exit(0)
        print("\n")
        return 


    # Parsing the file placed.sqlite and output the Search History
    def print_search_engine(places_db):
        try:
            conn = sqlite3.connect(places_db)
            c = conn.cursor()
            c.execute("select url, datetime(visit_date/1000000, 'unixepoch') from moz_places, moz_historyvisits \
                    where visit_count > 0 and moz_places.id==moz_historyvisits.place_id;")
        except Exception(e):
            if 'encrypted' in str(e):
                print('\n[*] Error reading your cookies database.')
                print('[*] Upgrade your Python-Sqlite3 Library')
                sys.exit(0)
                
        print('\n[*] -- Search Engine History --')
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
                    print('[+] ' + date + ' - Searched Baidu For: ' + search)
        # Bing
        for row in c:
            url = str(row[0])
            date = str(row[1])
            if 'bing' in url.lower():
                r = re.findall(r'q=.*\&', url)
                if r:
                    search = r[0].split('&')[0]
                    search = search.replace('q=', '').replace('+', ' ')
                    print('[+] ' + date + ' - Searched Bing For: ' + search)
        
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
                    print('[+] '+ date + ' - Searched Google For: ' + search)
        
        # Duckduckgo
        for row in c:
            url = str(row[0])
            date = str(row[1])
            if 'duckduckgo' in url.lower():
                r = re.findall(r'q=.*\&', url)
                if r:
                    search = r[0].split('&')[0]
                    search = search.replace('q=', '').replace('+', ' ')
                    print('[+] ' + date + ' - Searched Duckduckgo For: ' + search)
        
        # Yandex
        for row in c:
            url = str(row[0])
            date = str(row[1])
            if 'yandex' in url.lower():
                r = re.findall(r'text=.*\&', url)
                if r:
                    search = r[0].split('&')[0]
                    search = search.replace('text=', '').replace('+', ' ')
                    print('[+] ' + date + ' - Searched Yandex For: ' + search)

        # Startpage
        for row in c:
            url = str(row[0])
            date = str(row[1])
            if 'startpage' in url.lower():
                r = re.findall(r'q=.*\&', url)
                if r:
                    search = r[0].split('&')[0]
                    search = search.replace('q=', '').replace('+', ' ')
                    print('[+] ' + date + ' - Searched Startpage For: ' + search)

        # Sougou
        for row in c:
            url = str(row[0])
            date = str(row[1])
            if 'sogou' in url.lower():
                r = re.findall(r'query=.*\&', url)
                if r:
                    search = r[0].split('&')[0]
                    search = search.replace('query=', '').replace('+', ' ')
                    print('[+] ' + date + ' - Searched For: ' + search)

        # WikiPedia
        for row in c:
            url = str(row[0])
            date = str(row[1])
            if 'wikipedia' in url.lower():
                r = re.findall(r'wd=.*\&', url)
                if r:
                    search = r[0].split('&')[0]
                    search = search.replace('wd=', '').replace('+', ' ')
                    print('[+] ' + date + ' - Searched For: ' + search)

        print("\n")
        return 


    # Parsing the file places.sqlite and output the Bookmark Names and URLs
    def print_bookmark(places_db):
        try:
            conn = sqlite3.connect(places_db)
            c = conn.cursor()
        except Exception(e):
            if 'encrypted' in str(e):
                print('\n[*] Error reading your cookies database.')
                print('[*] Upgrade your Python-Sqlite3 Library')
                sys.exit(0)
                
        print('\n[*] --- Bookmarks --- ')
        # Google or 谷歌
        print("-- Bookmark names contains keyword \"Google\" or \"谷歌\" --")
        c.execute("select title from moz_bookmarks")
        for row in c:
            title = str(row[0])
            if 'google' in title.lower():
                print('[+] ' + title)
        print("\n")
        print("-- Bookmark URLs contains keyword \"Google\" --")
        c.execute("select * from moz_places")
        for row in c:
            url = str(row[1])
            if 'google' in url.lower():
                url = urllib.parse.unquote(url)
                print('[+] ' + url)
        print("\n")

        # Baidu or 百度
        print("-- Bookmark names contains keyword \"Baidu\" or \"百度\" --")
        c.execute("select title from moz_bookmarks")
        for row in c:
            title = str(row[0])
            if 'baidu' in title.lower():
                print('[+] ' + title)
            if '百度' in title.lower():
                print('[+] ' + title)
        print("\n")
        print("-- Bookmark URLs contains keyword \"Baidu\" --")
        c.execute("select * from moz_places")
        for row in c:
            url = str(row[1])
            if 'baidu' in url.lower():
                url = urllib.parse.unquote(url)
                print('[+] ' + url)
        print("\n")

        # Bing or 必应
        print("-- Bookmark names contains keyword \"Bing\" or \"必应\" --")
        c.execute("select title from moz_bookmarks")
        for row in c:
            title = str(row[0])
            if 'bing' in title.lower():
                print('[+] ' + title)
            if '必应' in title.lower():
                print('[+] ' + title)
        print("\n")
        print("-- Bookmark URLs contains keyword \"Bing\" --")
        c.execute("select * from moz_places")
        for row in c:
            url = str(row[1])
            if 'bing' in url.lower():
                url = urllib.parse.unquote(url)
                print('[+] ' + url)
        print("\n")
        
        # Wikipedia or 维基
        print("-- Bookmark names contains keyword \"Wikipedia\" or \"维基\" --")
        c.execute("select title from moz_bookmarks")
        for row in c:
            title = str(row[0])
            if 'wikipedia' in title.lower():
                print('[+] ' + title)
            if '维基' in title.lower():
                print('[+] ' + title)
        print("\n")
        
        print("-- Bookmark URLs contains keyword \"Wikipedia\" --")
        c.execute("select * from moz_places")
        for row in c:
            url = str(row[1])
            if 'wikipedia' in url.lower():
                url = urllib.parse.unquote(url)
                print('[+] ' + url)
        print("\n")

        # mail or 邮箱
        print("-- Bookmark names contains keyword \"Mail\" or \"邮箱\" --")
        c.execute("select title from moz_bookmarks")
        for row in c:
            title = str(row[0])
            if 'mail' in title.lower():
                print('[+] ' + title)
            if '邮箱' in title.lower():
                print('[+] ' + title)
        print("\n")
        
        print("-- Bookmark URLs contains keyword \"Mail\" --")
        c.execute("select * from moz_places")
        for row in c:
            url = str(row[1])
            if 'mail' in url.lower():
                url = urllib.parse.unquote(url)
                print('[+] ' + url)
        print("\n")

        # Youtube or 油管
        print("-- Bookmark names contains keyword \"Youtube\" or \"油管\" --")
        c.execute("select title from moz_bookmarks")
        for row in c:
            title = str(row[0])
            if 'youtube' in title.lower():
                print('[+] ' + title)
            if '油管' in title.lower():
                print('[+] ' + title)
        print("\n")
        
        print("-- Bookmark URLs contains keyword \"Youtube\" --")
        c.execute("select * from moz_places")
        for row in c:
            url = str(row[1])
            if 'youtube' in url.lower():
                url = urllib.parse.unquote(url)
                print('[+] ' + url)
        print("\n")


        # VPN
        print("-- Bookmark names contains keyword \"VPN\" --")
        c.execute("select title from moz_bookmarks")
        for row in c:
            title = str(row[0])
            if 'vpn' in title.lower():
                print('[+] ' + title)
        print("\n")
        
        print("-- Bookmark URLs contains keyword \"VPN\" --")
        c.execute("select * from moz_places")
        for row in c:
            url = str(row[1])
            if 'vpn' in url.lower():
                url = urllib.parse.unquote(url)
                print('[+] ' + url)
        print("\n")
        return


    def customized_print_cookies(cookies_db, customized_keyword):
        try:
            conn = sqlite3.connect(cookies_db)
            c = conn.cursor()
            c.execute('SELECT host, name, value FROM moz_cookies')

            print('\n\n[*] -- Cookies from customized keywords list --')
            for row in c:
                host = str(row[0])
                name = str(row[1])
                value = str(row[2])
                # print('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value)
                for keyword in customized_keyword:
                    if keyword.lower() in host.lower():
                        print('[+] Host hint keyword \"' + keyword.strip() + '\":' \
                            + host + ', Cookie: ' + name + ', Value: ' + value)

        except Exception(e):
            if 'encrypted' in str(e):
                print('\n[*] Error reading your cookies database.')
                print('[*] Upgrade your Python-Sqlite3 Library')
        print('\n')
        return


    def customized_print_history(places_db, customized_keyword):
        try:
            conn = sqlite3.connect(places_db)
            c = conn.cursor()
            c.execute("select url, datetime(visit_date/1000000, 'unixepoch') from moz_places, moz_historyvisits \
                    where visit_count > 0 and moz_places.id==moz_historyvisits.place_id;")

            print('\n[*] -- Browsing History from customized keywords list --')
            for row in c:
                url = str(row[0])
                date = str(row[1])
                for keyword in customized_keyword:
                    if keyword.lower() in url.lower():
                        print('[+] Browsing history hint keyword \"' + keyword + '\":' 
                            + date + ' - Visited: ' + url)
                
        except Exception(e):
            if 'encrypted' in str(e):
                print('\n[*] Error reading your places database.')
                print('[*] Upgrade your Python-Sqlite3 Library')
                sys.exit(0)
        print("\n")
        return 

        
    def customized_print_downloads(download_db, customized_keyword):
        conn = sqlite3.connect(download_db)
        c = conn.cursor()
        c.execute('SELECT name, source, datetime(endTime/1000000, \'unixepoch\') FROM moz_downloads;')
        print('\n[*] -- File download record from customized keywords list -- ')
        for row in c:
            for keyword in customized_keyword:
                if keyword.lower() in row.lower():
                    print('[+] File hint keyword \"' + keyword.strip() + '\"' 
                        + str(row[0]) + ' from source: ' + str(row[1]) + ' at: ' + str(row[2]))
        print("\n\n")
        return 


    # Parsing the bookmark by customized keywords
    def customized_print_bookmark(places_db, customized_keyword):
        try:
            conn = sqlite3.connect(places_db)
            c = conn.cursor()
        except Exception(e):
            if 'encrypted' in str(e):
                print('\n[*] Error reading your cookies database.')
                print('[*] Upgrade your Python-Sqlite3 Library')
                sys.exit(0)   

        print("-- Bookmark from customized keywords list --")
        print(customized_keyword)
        c.execute("select title from moz_bookmarks")
        for row in c:
            title = str(row[0])
            for i in customized_keyword:
                i = i.lower()
                if i in title.lower():
                    print('[+] ' + title)
        print("\n")
        print("[*] -- Bookmark URLs that contain customized keyword --")
        c.execute("select * from moz_places")
        for row in c:
            url = str(row[1])
            for keyword in customized_keyword:
                keyword = i.lower()
                if keyword in url.lower():
                    url = urllib.parse.unquote(url)
                    print('[+] Bookmark hint keyword \"' + keyword.strip() + '\": '+ url)
        print("\n")

        return   


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
            print ("[*] Error reading bookmark file: " + bookmark_file)
            return
        print("[*] -- Bookmarks --")
        for bookmark in bookmark_json["roots"]["bookmark_bar"]["children"]:
            print(bookmark["name"] + ': ' + bookmark["url"])
        return


    def print_history(history_db):
        conn = sqlite3.connect(history_db)
        c = conn.cursor()
        c.execute("SELECT id,url,title,visit_count,last_visit_time  from urls")
        print('\n\n\n[*] -- Browsing History --')
        for _id, url, title, visit_count, last_visit_time in c:
            time = str(Chromium.get_chrome_datetime(last_visit_time))
            print('[+] ' + time + ' Visited ' + title + ': ' + url)
        return


    def print_search_engine(history_db):
        conn = sqlite3.connect(history_db)
        c = conn.cursor()
        c.execute("SELECT normalized_term FROM keyword_search_terms;")
        print('\n\n\n[*] -- Search Engine Record -- ')
        for row in c:
            print('[+] Search Record: ' + str(row))
        return


    def print_downloads(download_db):
        conn = sqlite3.connect(download_db)
        c = conn.cursor()
        c.execute("SELECT url FROM downloads_url_chains;")
        print('\n\n\n[*] -- Files Downloaded -- ')
        for row in c:
            print('[+] File: ' + str(row))
        return


    def customized_print_bookmark(bookmark_file, customized_keyword):
        try:
            with open(bookmark_file, 'r', encoding='utf-8') as input_bookmark:
                bookmark_content = input_bookmark.read()
                bookmark_json = json.loads(bookmark_content)
        except:
            print ("[*] Error reading bookmark file: " + bookmark_file)
            return
        
        print("\n\n[*] -- Bookmarks that hint customized keywords --")
        for bookmark in bookmark_json["roots"]["bookmark_bar"]["children"]:
            for keyword in customized_keyword:
                if keyword.lower() in bookmark["name"].lower() or keyword.lower() in bookmark["url"].lower():
                    print('[+] Bookmark hint keyword \"' + keyword.strip() + '\": '+ bookmark["name"] + ' ' + bookmark["url"])
        return


    def customized_print_history(history_db, customized_keyword):
        conn = sqlite3.connect(history_db)
        c = conn.cursor()
        c.execute("SELECT id,url,title,visit_count,last_visit_time  from urls")
        print('\n\n\n[*] -- Browsing History that contain customized keyword --')
        for _id, url, title, visit_count, last_visit_time in c:
            time = str(Chromium.get_chrome_datetime(last_visit_time))
            for keyword in customized_keyword:
                if keyword.lower() in title.lower() or keyword.lower() in url.lower():
                    print('[+] ' + time + ' Visite History hint keyword \"' + keyword.strip() + '\": '+ title + ', ' + url)
        return


    def customized_print_search_engine(history_db, customized_keyword):
        conn = sqlite3.connect(history_db)
        c = conn.cursor()
        c.execute("SELECT normalized_term FROM keyword_search_terms;")
        print('\n[*] -- Search engine record that hint customized keywords -- ')
        for row in c:
            for keyword in customized_keyword:
                if keyword.lower() in row[0].lower():
                    print('[+] Search Record hint keyword \"' + keyword + '\": ' + str(row))
        return


    def customized_print_downloads(download_db, customized_keyword):
        conn = sqlite3.connect(download_db)
        c = conn.cursor()
        c.execute("SELECT url FROM downloads_url_chains;")
        print('\n\n[*] -- Files Downloaded that hint customized keywords -- ')
        for row in c:
            for keyword in customized_keyword:
                if keyword.lower() in row[0].lower():
                    print('[+] File hint keyword \"' + keyword + '\": ' + str(row))
        return
    


# Main function
def main():
    parser = optparse.OptionParser("[*] Usage: main.py -b <Browser Version> -p <Browser profile path> -k <Custom keyword dictionary>")
    parser.add_option('-b', dest = 'browser_version', type = 'string', help = 'Specify browser version (Firefox or Chromium)')
    parser.add_option('-p', dest = 'path_name', type = 'string', help = 'Specify Browser profile path')
    parser.add_option('-k', dest = 'custom_keyword', type = 'string', help = 'Specify custom keyword dictionary file')
    (options, args) = parser.parse_args()

    path_name = options.path_name
    custom_keyword_place = options.custom_keyword
    browser_version = options.browser_version

    if browser_version == None:
        print(parser.usage)
        sys.exit(0)
    elif os.path.isdir(path_name) == False:
        print('[!] Path Does Not Exist: ' + path_name)
        raise Exception("PathNotExist")
        sys.exit(0)

    # Browser_version: Firefox
    elif browser_version == 'Firefox':
        if path_name == None:
            print(parser.usage)
            sys.sys.exit(0)
        elif os.path.isdir(path_name) == False:
            print('[!] Path Does Not Exist: ' + path_name)
            raise Exception("PathNotExist")
            sys.exit(0)
        else:
            download_db = os.path.join(path_name, 'downloads.sqlite')
            if os.path.isfile(download_db):
                Firefox.print_downloads(download_db)

                # Detect whether parameter -k is specified
                if custom_keyword_place == None:
                    pass
                elif os.path.isfile(custom_keyword_place) == False:
                    print('[!] Path Does Not Exist: ' + custom_keyword_place)
                    raise Exception("PathNotExist")
                else:
                    with open (custom_keyword_place, encoding='utf-8') as keyword_file:
                        custom_keyword = keyword_file.readlines()
                        custom_keyword = [line.rstrip() for line in custom_keyword]
                        if custom_keyword == []:
                            print("[!] Keyword List Empty! Passing Now... \n\n")
                        else:
                            Firefox.customized_print_downloads(download_db, custom_keyword)
            else:
                print('[!] Downloads Db (downloads.sqlite) does not exist: '+ download_db)

            # cookies.sqlite
            cookies_db = os.path.join(path_name, 'cookies.sqlite')
            if os.path.isfile(cookies_db):
                Firefox.print_cookies(cookies_db)

                # Detect whether parameter -k is specified
                if custom_keyword_place == None:
                    pass
                elif os.path.isfile(custom_keyword_place) == False:
                    print('[!] Path Does Not Exist: ' + custom_keyword_place)
                    raise Exception("PathNotExist")
                else:
                    with open (custom_keyword_place, encoding='utf-8') as keyword_file:
                        custom_keyword = keyword_file.readlines()
                        custom_keyword = [line.rstrip() for line in custom_keyword]
                        if custom_keyword == []:
                            print("[!] Keyword List Empty! Passing Now... \n\n")
                        else:
                            Firefox.customized_print_cookies(cookies_db, custom_keyword)

            else:
                print('[!] Cookies Db (cookies.sqlite) does not exist:' + cookies_db)
            
            # places.sqlite
            places_db = os.path.join(path_name, 'places.sqlite')
            if os.path.isfile(places_db):

                Firefox.print_history(places_db)
                # Detect whether parameter -k is specified
                if custom_keyword_place == None:
                    pass
                elif os.path.isfile(custom_keyword_place) == False:
                    print('[!] Path Does Not Exist: ' + custom_keyword_place)
                    raise Exception("PathNotExist")
                else:
                    with open (custom_keyword_place, encoding='utf-8') as keyword_file:
                        custom_keyword = keyword_file.readlines()
                        custom_keyword = [line.rstrip() for line in custom_keyword]
                        if custom_keyword == []:
                            print("[!] Keyword List Empty! Passing Now... \n\n")
                        else:
                            Firefox.customized_print_history(places_db, custom_keyword)

                Firefox.print_search_engine(places_db)

                Firefox.print_bookmark(places_db)
                # Detect whether parameter -k is specified
                if custom_keyword_place == None:
                    pass
                elif os.path.isfile(custom_keyword_place) == False:
                    print('[!] Path Does Not Exist: ' + custom_keyword_place)
                    raise Exception("PathNotExist")
                else:
                    with open (custom_keyword_place, encoding='utf-8') as keyword_file:
                        custom_keyword = keyword_file.readlines()
                        custom_keyword = [line.rstrip() for line in custom_keyword]
                        if custom_keyword == []:
                            print("[!] Keyword List Empty! Passing Now... \n\n")
                        else:
                            Firefox.customized_print_bookmark(places_db, custom_keyword)
            else:
                print('[!] places_db (places.db) does not exist: ' + places_db)

        print("[*] Firefox Analyzing Completed! ")
        return
    
    # Browser_version: Chromium
    elif browser_version == 'Chromium':
        if path_name == None:
            print(parser.usage)
            sys.exit(0)
        elif os.path.isdir(path_name) == False:
            print('[!] Path Does Not Exist: ' + path_name)
            raise Exception("PathNotExist")
            sys.exit(0)
        else:
            # Bookmarks
            bookmark_location = os.path.join(path_name, 'Bookmarks')
            Chromium.print_bookmark(bookmark_location)
            # Detect whether parameter -k is specified
            if custom_keyword_place == None:
                pass
            elif os.path.isfile(custom_keyword_place) == False:
                print('[!] Path Does Not Exist: ' + custom_keyword_place)
                raise Exception("PathNotExist")
            else:
                with open (custom_keyword_place, encoding='utf-8') as keyword_file:
                    custom_keyword = keyword_file.readlines()
                    custom_keyword = [line.rstrip() for line in custom_keyword]
                    if custom_keyword == []:
                        print("[!] Keyword List Empty! Passing Now... \n\n")
                    else:
                        Chromium.customized_print_bookmark(bookmark_location, custom_keyword)            

            # Downloads
            history_location = os.path.join(path_name, 'History')
            Chromium.print_downloads(history_location)
            # Detect whether parameter -k is specified
            if custom_keyword_place == None:
                pass
            elif os.path.isfile(custom_keyword_place) == False:
                print('[!] Path Does Not Exist: ' + custom_keyword_place)
                raise Exception("PathNotExist")
            else:
                with open (custom_keyword_place, encoding='utf-8') as keyword_file:
                    custom_keyword = keyword_file.readlines()
                    custom_keyword = [line.rstrip() for line in custom_keyword]
                    if custom_keyword == []:
                        print("[!] Keyword List Empty! Passing Now... \n\n")
                    else:
                        Chromium.customized_print_downloads(history_location, custom_keyword)

            # Search History
            Chromium.print_search_engine(history_location)
            # Detect whether parameter -k is specified
            if custom_keyword_place == None:
                pass
            elif os.path.isfile(custom_keyword_place) == False:
                print('[!] Path Does Not Exist: ' + custom_keyword_place)
                raise Exception("PathNotExist")
            else:
                with open (custom_keyword_place, encoding='utf-8') as keyword_file:
                    custom_keyword = keyword_file.readlines()
                    custom_keyword = [line.rstrip() for line in custom_keyword]
                    if custom_keyword == []:
                        print("[!] Keyword List Empty! Passing Now... \n\n")
                    else:
                        Chromium.customized_print_search_engine(history_location, custom_keyword)

            # History
            Chromium.print_history(history_location)
            # Detect whether parameter -k is specified
            if custom_keyword_place == None:
                pass
            elif os.path.isfile(custom_keyword_place) == False:
                print('[!] Path Does Not Exist: ' + custom_keyword_place)
                raise Exception("PathNotExist")
            else:
                with open (custom_keyword_place, encoding='utf-8') as keyword_file:
                    custom_keyword = keyword_file.readlines()
                    custom_keyword = [line.rstrip() for line in custom_keyword]
                    if custom_keyword == []:
                        print("[!] Keyword List Empty! Passing Now... \n\n")
                    else:
                        Chromium.customized_print_history(history_location, custom_keyword)
            return
            
    # Other situations
    else:
        print(parser.usage)


if __name__ == '__main__':
    main()
    sys.exit(0)