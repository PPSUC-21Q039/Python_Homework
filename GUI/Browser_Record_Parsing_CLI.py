# coding=utf-8
#########################################################################
# File Name: Browser_Record_Parsing_CLI.py
# Author: Wenqiang Hu
# E-mail: huwenqiang.hwq@protonmail.com
# Created Time: 11/5/2022 10:57:13
# Description: See Readme.md
# CALL Help:
#   Browser_Record_Parsing_CLI.main(path_name = '', browser_version = '', custom_keyword_place = ''),
#   path_name is a string that specifies the path of profile directory,
#   browser_version should be 'Firefox' or 'Chromium',
#   custom_keyword_place is a optional parameter that specifies the custom keyword file location.
########################################################################


import re
import os
import json
import sqlite3
import optparse
import urllib.parse  # Decode the URL Code
from datetime import datetime, timedelta
from tkinter import messagebox

# Change the Default Encoding 
import io
import sys
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
OUTPUT_FILE = "./output.txt"
OUTPUT = open(OUTPUT_FILE, "w", encoding="utf8")

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
                sys.exit(0)
                
        print('\n[*] --- Bookmarks --- ')
        print('\n[*] --- Bookmarks --- ', file = OUTPUT)
        
        # All
        print("-- All Bookmark Names --")
        print("-- All Bookmark Names --", file = OUTPUT)
        c.execute("select title from moz_bookmarks")
        for row in c:
            title = str(row[0])
            print('[+] ' + title)
        print("\n")
        print("-- All Bookmark URLs --")
        print("\n", file = OUTPUT)
        print("-- All Bookmark URLs --", file = OUTPUT)
        c.execute("select * from moz_places")
        for row in c:
            url = str(row[1])
            #url = urllib.parse.unquote(url)
            print('[+] ' + url)
            print('[+] ' + url, file = OUTPUT)
        print("\n")
        print("\n", file = OUTPUT)
        
        # Google or 谷歌
        print("-- Bookmark names contains keyword \"Google\" or \"谷歌\" --")
        print("-- Bookmark names contains keyword \"Google\" or \"谷歌\" --", file = OUTPUT)
        c.execute("select title from moz_bookmarks")
        for row in c:
            title = str(row[0])
            if 'google' in title.lower():
                print('[+] ' + title)
                print('[+] ' + title, file = OUTPUT)
        print("\n")
        print("\n", file = OUTPUT)
        print("-- Bookmark URLs contains keyword \"Google\" --")
        print("-- Bookmark URLs contains keyword \"Google\" --", file = OUTPUT)
        c.execute("select * from moz_places")
        for row in c:
            url = str(row[1])
            if 'google' in url.lower():
                # url = urllib.parse.unquote(url)
                print('[+] ' + url)
                print('[+] ' + url, file = OUTPUT)
        print("\n")
        print("\n", file = OUTPUT)

        # Baidu or 百度
        print("-- Bookmark names contains keyword \"Baidu\" or \"百度\" --")
        print("-- Bookmark names contains keyword \"Baidu\" or \"百度\" --", file = OUTPUT)
        c.execute("select title from moz_bookmarks")
        for row in c:
            title = str(row[0])
            
            if 'baidu' in title.lower():
                print('[+] ' + title)
                print('[+] ' + title, file = OUTPUT)
            if '百度' in title.lower():
                print('[+] ' + title)
                # print('[+] ' + title, file = OUTPUT)
        print("\n")
        print("\n", file = OUTPUT)
        print("-- Bookmark URLs contains keyword \"Baidu\" --")
        print("-- Bookmark URLs contains keyword \"Baidu\" --", file = OUTPUT)
        c.execute("select * from moz_places")
        for row in c:
            url = str(row[1])
            if 'baidu' in url.lower():
                # url = urllib.parse.unquote(url)
                print('[+] ' + url)
                print('[+] ' + url, file = OUTPUT)
        print("\n")
        print("\n", file = OUTPUT)

        # Bing or 必应
        print("-- Bookmark names contains keyword \"Bing\" or \"必应\" --")
        print("-- Bookmark names contains keyword \"Bing\" or \"必应\" --", file = OUTPUT)
        c.execute("select title from moz_bookmarks")
        for row in c:
            title = str(row[0])
            if 'bing' in title.lower():
                print('[+] ' + title)
                print('[+] ' + title, file = OUTPUT)
            if '必应' in title.lower():
                print('[+] ' + title)
                print('[+] ' + title, file = OUTPUT)
        print("\n")
        print("\n", file = OUTPUT)
        print("-- Bookmark URLs contains keyword \"Bing\" --")
        print("-- Bookmark URLs contains keyword \"Bing\" --", file = OUTPUT)
        c.execute("select * from moz_places")
        for row in c:
            url = str(row[1])
            if 'bing' in url.lower():
                url = urllib.parse.unquote(url)
                print('[+] ' + url)
                print('[+] ' + url, file = OUTPUT)
        print("\n")
        print("\n", file = OUTPUT)
        
        # Wikipedia or 维基
        print("-- Bookmark names contains keyword \"Wikipedia\" or \"维基\" --")
        print("-- Bookmark names contains keyword \"Wikipedia\" or \"维基\" --", file = OUTPUT)
        c.execute("select title from moz_bookmarks")
        for row in c:
            title = str(row[0])
            if 'wikipedia' in title.lower():
                print('[+] ' + title)
                print('[+] ' + title, file = OUTPUT)
            if '维基' in title.lower():
                print('[+] ' + title)
                print('[+] ' + title, file = OUTPUT)
        print("\n")
        print("\n", file = OUTPUT)
        
        print("-- Bookmark URLs contains keyword \"Wikipedia\" --")
        print("-- Bookmark URLs contains keyword \"Wikipedia\" --", file = OUTPUT)
        c.execute("select * from moz_places")
        for row in c:
            url = str(row[1])
            if 'wikipedia' in url.lower():
                # url = urllib.parse.unquote(url)
                print('[+] ' + url)
                print('[+] ' + url, file = OUTPUT)
        print("\n")
        print("\n", file = OUTPUT)

        # mail or 邮箱
        print("-- Bookmark names contains keyword \"Mail\" or \"邮箱\" --")
        print("-- Bookmark names contains keyword \"Mail\" or \"邮箱\" --", file = OUTPUT)
        c.execute("select title from moz_bookmarks")
        for row in c:
            title = str(row[0])
            if 'mail' in title.lower():
                print('[+] ' + title)
                print('[+] ' + title, file = OUTPUT)
            if '邮箱' in title.lower():
                print('[+] ' + title)
                print('[+] ' + title, file = OUTPUT)
        print("\n")
        print("\n", file = OUTPUT)
        
        print("-- Bookmark URLs contains keyword \"Mail\" --")
        print("-- Bookmark URLs contains keyword \"Mail\" --", file = OUTPUT)
        c.execute("select * from moz_places")
        for row in c:
            url = str(row[1])
            if 'mail' in url.lower():
                # url = urllib.parse.unquote(url)
                print('[+] ' + url)
                print('[+] ' + url, file = OUTPUT)
        print("\n")
        print("\n", file = OUTPUT)

        # YouTube or 油管
        print("-- Bookmark names contains keyword \"Youtube\" or \"油管\" --")
        print("-- Bookmark names contains keyword \"Youtube\" or \"油管\" --", file = OUTPUT)
        c.execute("select title from moz_bookmarks")
        for row in c:
            title = str(row[0])
            if 'youtube' in title.lower():
                print('[+] ' + title)
                print('[+] ' + title, file = OUTPUT)
            if '油管' in title.lower():
                print('[+] ' + title)
                print('[+] ' + title, file = OUTPUT)
        print("\n")
        print("\n", file = OUTPUT)
        
        print("-- Bookmark URLs contains keyword \"Youtube\" --")
        print("-- Bookmark URLs contains keyword \"Youtube\" --", file = OUTPUT)
        c.execute("select * from moz_places")
        for row in c:
            url = str(row[1])
            if 'youtube' in url.lower():
                # url = urllib.parse.unquote(url)
                print('[+] ' + url)
                print('[+] ' + url, file = OUTPUT)
        print("\n")
        print("\n", file = OUTPUT)


        # VPN
        print("-- Bookmark names contains keyword \"VPN\" --")
        print("-- Bookmark names contains keyword \"VPN\" --", file = OUTPUT)
        c.execute("select title from moz_bookmarks")
        for row in c:
            title = str(row[0])
            if 'vpn' in title.lower():
                print('[+] ' + title)
                print('[+] ' + title, file = OUTPUT)
        print("\n")
        print("\n", file = OUTPUT)
        
        print("-- Bookmark URLs contains keyword \"VPN\" --")
        print("-- Bookmark URLs contains keyword \"VPN\" --", file = OUTPUT)
        c.execute("select * from moz_places")
        for row in c:
            url = str(row[1])
            if 'vpn' in url.lower():
                # url = urllib.parse.unquote(url)
                print('[+] ' + url)
                print('[+] ' + url, file = OUTPUT)
        print("\n")
        print("\n", file = OUTPUT)
        return
    
    
    def customized_print_cookies(cookies_db, customized_keyword):
        try:
            conn = sqlite3.connect(cookies_db)
            c = conn.cursor()
            c.execute('SELECT host, name, value FROM moz_cookies')

            print('\n\n[*] -- Cookies from customized keywords list --')
            print('\n\n[*] -- Cookies from customized keywords list --', file = OUTPUT)
            for row in c:
                host = str(row[0])
                name = str(row[1])
                value = str(row[2])
                # print('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value)
                for keyword in customized_keyword:
                    if keyword.lower() in host.lower():
                        print('[+] Host hint keyword \"' + keyword.strip() + '\":' \
                            + host + ', Cookie: ' + name + ', Value: ' + value)
                        print('[+] Host hint keyword \"' + keyword.strip() + '\":' \
                            + host + ', Cookie: ' + name + ', Value: ' + value, file = OUTPUT)

        except Exception as e:
            if 'encrypted' in str(e):
                print('\n[*] Error reading your cookies database.')
                print('[*] Upgrade your Python-Sqlite3 Library')
                print('\n[*] Error reading your cookies database.', file = OUTPUT)
                print('[*] Upgrade your Python-Sqlite3 Library', file = OUTPUT)
        print('\n')
        print('\n', file = OUTPUT)
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
                        print('[+] Browsing history hint keyword \"' + keyword + '\":' 
                            + date + ' - Visited: ' + url, file = OUTPUT)
                
        except Exception as e:
            if 'encrypted' in str(e):
                print('\n[*] Error reading your places database.')
                print('[*] Upgrade your Python-Sqlite3 Library')
                print('\n[*] Error reading your places database.', file = OUTPUT)
                print('[*] Upgrade your Python-Sqlite3 Library', file = OUTPUT)
                sys.exit(0)
        print("\n")
        return 

        
    def customized_print_downloads(download_db, customized_keyword):
        conn = sqlite3.connect(download_db)
        c = conn.cursor()
        c.execute('SELECT name, source, datetime(endTime/1000000, \'unixepoch\') FROM moz_downloads;')
        print('\n[*] -- File download record from customized keywords list -- ')
        print('\n[*] -- File download record from customized keywords list -- ', file = OUTPUT)
        for row in c:
            for keyword in customized_keyword:
                if keyword.lower() in row.lower():
                    print('[+] File hint keyword \"' + keyword.strip() + '\"' 
                        + str(row[0]) + ' from source: ' + str(row[1]) + ' at: ' + str(row[2]))
                    print('[+] File hint keyword \"' + keyword.strip() + '\"' 
                        + str(row[0]) + ' from source: ' + str(row[1]) + ' at: ' + str(row[2]), file = OUTPUT)
        print("\n\n")
        print("\n\n", file = OUTPUT)
        return 


    # Parsing the bookmark by customized keywords
    def customized_print_bookmark(places_db, customized_keyword):
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

        print("-- Bookmark from customized keywords list --")
        print("-- Bookmark from customized keywords list --", file = OUTPUT)
        print(customized_keyword)
        print(customized_keyword, file = OUTPUT)
        c.execute("select title from moz_bookmarks")
        for row in c:
            title = str(row[0])
            for i in customized_keyword:
                i = i.lower()
                if i in title.lower():
                    print('[+] ' + title)
                    print('[+] ' + title, file = OUTPUT)
        print("\n")
        print("\n", file = OUTPUT)
        print("[*] -- Bookmark URLs that contain customized keyword --")
        print("[*] -- Bookmark URLs that contain customized keyword --", file = OUTPUT)
        c.execute("select * from moz_places")
        for row in c:
            url = str(row[1])
            for keyword in customized_keyword:
                keyword = i.lower()
                if keyword in url.lower():
                    url = urllib.parse.unquote(url)
                    print('[+] Bookmark hint keyword \"' + keyword.strip() + '\": '+ url)
                    print('[+] Bookmark hint keyword \"' + keyword.strip() + '\": '+ url, file = OUTPUT)
        print("\n")
        print("\n", file = OUTPUT)

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
            print("[*] Error reading bookmark file: " + bookmark_file)
            print("[*] Error reading bookmark file: " + bookmark_file, file = OUTPUT)
            return
        print("[*] -- Bookmarks --", file = OUTPUT)
        for bookmark in bookmark_json["roots"]["bookmark_bar"]["children"]:
            print(bookmark["name"] + ': ' + bookmark["url"])
            print(bookmark["name"] + ': ' + bookmark["url"], file = OUTPUT)
        return

    def print_history(history_db):
        conn = sqlite3.connect(history_db)
        c = conn.cursor()
        c.execute("SELECT id,url,title,visit_count,last_visit_time  from urls")
        print('\n\n\n[*] -- Browsing History --')
        print('\n\n\n[*] -- Browsing History --', file = OUTPUT)
        for _id, url, title, visit_count, last_visit_time in c:
            time = str(Chromium.get_chrome_datetime(last_visit_time))
            print('[+] ' + time + ' Visited: ' + title + ': ' + url)
            print('[+] ' + time + ' Visited: ' + title + ': ' + url, file = OUTPUT)
        return

    def print_search_engine(history_db):
        conn = sqlite3.connect(history_db)
        c = conn.cursor()
        c.execute("SELECT normalized_term FROM keyword_search_terms;")
        print('\n\n\n[*] -- Search Engine Record -- ')
        print('\n\n\n[*] -- Search Engine Record -- ', file = OUTPUT)
        for row in c:
            print('[+] Search Record: ' + str(row))
            print('[+] Search Record: ' + str(row), file = OUTPUT)
        return

    def print_downloads(download_db):
        conn = sqlite3.connect(download_db)
        c = conn.cursor()
        c.execute("SELECT url FROM downloads_url_chains;")
        print('\n\n\n[*] -- Files Downloaded -- ')
        print('\n\n\n[*] -- Files Downloaded -- ', file = OUTPUT)
        for row in c:
            print('[+] File: ' + str(row))
            print('[+] File: ' + str(row), file = OUTPUT)
        return

    def customized_print_bookmark(bookmark_file, customized_keyword):
        try:
            with open(bookmark_file, 'r', encoding='utf-8') as input_bookmark:
                bookmark_content = input_bookmark.read()
                bookmark_json = json.loads(bookmark_content)
        except:
            print("[*] Error reading bookmark file: " + bookmark_file)
            print("[*] Error reading bookmark file: " + bookmark_file, file = OUTPUT)
            return

        print("\n\n[*] -- Bookmarks that hint customized keywords --")
        print("\n\n[*] -- Bookmarks that hint customized keywords --", file = OUTPUT)
        for bookmark in bookmark_json["roots"]["bookmark_bar"]["children"]:
            for keyword in customized_keyword:
                if keyword.lower() in bookmark["name"].lower() or keyword.lower() in bookmark["url"].lower():
                    print('[+] Bookmark hnt keyword \"' + keyword.strip() + '\": ' + bookmark["name"] + ' ' + bookmark["url"])
                    print('[+] Bookmark hint keyword \"' + keyword.strip() + '\": ' + bookmark["name"] + ' ' + bookmark["url"], file = OUTPUT)
        return

    def customized_print_history(history_db, customized_keyword):
        conn = sqlite3.connect(history_db)
        c = conn.cursor()
        c.execute("SELECT id,url,title,visit_count,last_visit_time  from urls")
        print('\n\n\n[*] -- Browsing History that contain customized keyword --')
        print('\n\n\n[*] -- Browsing History that contain customized keyword --', file = OUTPUT)
        for _id, url, title, visit_count, last_visit_time in c:
            time = str(Chromium.get_chrome_datetime(last_visit_time))
            for keyword in customized_keyword:
                if keyword.lower() in title.lower() or keyword.lower() in url.lower():
                    print('[+] ' + time + ' Visite History hint keyword \"' + keyword.strip() + '\": ' + title + ', ' + url)
                    print('[+] ' + time + ' Visite History hint keyword \"' + keyword.strip() + '\": ' + title + ', ' + url, file = OUTPUT)
        return

    def customized_print_search_engine(history_db, customized_keyword):
        conn = sqlite3.connect(history_db)
        c = conn.cursor()
        c.execute("SELECT normalized_term FROM keyword_search_terms;")
        print('\n[*] -- Search engine record that hint customized keywords -- ')
        print('\n[*] -- Search engine record that hint customized keywords -- ', file = OUTPUT)
        for row in c:
            for keyword in customized_keyword:
                if keyword.lower() in row[0].lower():
                    print('[+] Search Record hints keyword \"' + keyword + '\": ' + str(row))
                    print('[+] Search Record hints keyword \"' + keyword + '\": ' + str(row), file = OUTPUT)
        return

    def customized_print_downloads(download_db, customized_keyword):
        conn = sqlite3.connect(download_db)
        c = conn.cursor()
        c.execute("SELECT url FROM downloads_url_chains;")
        print('\n\n[*] -- Files Downloaded that hint customized keywords -- ')
        print('\n\n[*] -- Files Downloaded that hint customized keywords -- ', file = OUTPUT)
        for row in c:
            for keyword in customized_keyword:
                if keyword.lower() in row[0].lower():
                    print('[+] File hint keyword \"' + keyword + '\": ' + str(row))
                    print('[+] File hint keyword \"' + keyword + '\": ' + str(row), file = OUTPUT)
        return



# Main function
def main(path_name = '', browser_version = '', custom_keyword_place = ''):
    parser = optparse.OptionParser("Browser_Record_Parsing_CLI.py -b <Browser version (Firefox or Chromium)> -p <Browser profile path> -k <Custom keyword dictionary file>")
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
            sys.exit(0)
        elif os.path.isdir(path_name) == False:
            print('[!] Path Does Not Exist: ' + path_name)
            raise Exception("PathNotExist")
            sys.exit(0)
        else:
            download_db = os.path.join(path_name, 'downloads.sqlite')
            if os.path.isfile(download_db):
                Firefox.print_downloads(download_db)

                # Detect whether parameter -k is specified
                if custom_keyword_place == 'None':
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
                if custom_keyword_place == 'None':
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
                if custom_keyword_place == 'None':
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
                if custom_keyword_place == 'None':
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
        # messagebox.showinfo("Parsing", "Successfully analyzed Firefox records!\nClick Quit to end this process")
        messagebox_choice = messagebox.askokcancel("Parsing", "Successfully analyzed Firefox records!\nEnd this process now? ")
        if messagebox_choice == True:
            sys.exit(0)
        elif messagebox_choice == False:
            pass
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
            if custom_keyword_place == 'None':
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
            if custom_keyword_place == 'None':
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
            if custom_keyword_place == 'None':
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
            if custom_keyword_place == 'None':
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
            
            messagebox_choice = messagebox.askokcancel("Parsing", "Successfully analyzed Chromium records!\nEnd this process now? ")
            if messagebox_choice == True:
                sys.exit(0)
            elif messagebox_choice == False:
                pass
            return
            
    # Other situations
    else:
        print("Error! ")
        pause_operating = input()


if __name__ == '__main__':
    parser = optparse.OptionParser("Browser_Record_Parsing_CLI.py -b <Browser version (Firefox or Chromium)> -p <Browser profile path> -k <Custom keyword dictionary file>")
    parser.add_option('-b', dest = 'browser_version', type = 'string', help = 'Specify browser version (Firefox or Chromium)')
    parser.add_option('-p', dest = 'path_name', type = 'string', help = 'Specify browser profile path')
    parser.add_option('-k', dest = 'custom_keyword', type = 'string', help = 'Specify custom keyword dictionary file')
    (options, args) = parser.parse_args()

    path_name = options.path_name
    custom_keyword_place = options.custom_keyword
    browser_version = options.browser_version

    main(path_name = path_name, browser_version = browser_version, custom_keyword_place = str(custom_keyword_place))
    sys.exit(0)