#!/usr/bin/python
#coding=utf-8
import re
import optparse
import os
import sqlite3
import urllib.parse

# Change the Default Encoding
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

# Parse the file downloads.sqlite and output the download record
def print_downloads(downloadDB):
    conn = sqlite3.connect(downloadDB)
    c = conn.cursor()
    c.execute('SELECT name, source, datetime(endTime/1000000, \'unixepoch\') FROM moz_downloads;')
    print ('\n[*] --- Files Downloaded --- ')
    for row in c:
        print ('[+] File: ' + str(row[0]) + ' from source: ' + str(row[1]) + ' at: ' + str(row[2]))


# Parse the file cookies.sqlite and output the Cookies
def print_cookies(cookiesDB):
    try:
        conn = sqlite3.connect(cookiesDB)
        c = conn.cursor()
        c.execute('SELECT host, name, value FROM moz_cookies')

        print ('\n[*] -- Cookies --')
        for row in c:
            host = str(row[0])
            name = str(row[1])
            value = str(row[2])
            print ('[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value)
    except Exception(e):
        if 'encrypted' in str(e):
            print ('\n[*] Error reading your cookies database.')
            print ('[*] Upgrade your Python-Sqlite3 Library')


# Parse the file places.sqlite and output the History Record
def print_history(placesDB):
    try:
        conn = sqlite3.connect(placesDB)
        c = conn.cursor()
        c.execute("select url, datetime(visit_date/1000000, 'unixepoch') from moz_places, moz_historyvisits where visit_count > 0 and moz_places.id==moz_historyvisits.place_id;")

        print ('\n[*] -- Browsing History --')
        for row in c:
            url = str(row[0])
            date = str(row[1])
            print ('[+] ' + date + ' - Visited: ' + url)
    except Exception(e):
        if 'encrypted' in str(e):
            print ('\n[*] Error reading your places database.')
            print ('[*] Upgrade your Python-Sqlite3 Library')
            exit(0)


# Parse the file placed.sqlite and output the Search History
def print_search_engine(placesDB):
    conn = sqlite3.connect(placesDB)
    c = conn.cursor()
    c.execute("select url, datetime(visit_date/1000000, 'unixepoch') from moz_places, moz_historyvisits where visit_count > 0 and moz_places.id==moz_historyvisits.place_id;")

    print ('\n[*] -- Search Engine History --')
    # Baidu
    for row in c:
        url = str(row[0])
        date = str(row[1])
        if 'baidu' in url.lower():
            r = re.findall(r'wd=.*?\&', url)
            if r:
                search=r[0].split('&')[0]
                search=search.replace('wd=', '').replace('+', ' ')
                search = urllib.parse.unquote(search)
                print ('[+] ' + date + ' - Searched Baidu For: ' + search)
    # Bing
    for row in c:
        url = str(row[0])
        date = str(row[1])
        if 'bing' in url.lower():
            r = re.findall(r'q=*?\&', url)
            if r:
                search=r[0].split('&')[0]
                search=search.replace('q=', '').replace('+', ' ')
                print ('[+] ' + date + ' - Searched Bing For: ' + search)
    
    # Google
    for row in c:
        url = str(row[0])
        date = str(row[1])
        if 'google' in url.lower():
            r = re.findall(r'q=.*?\&', url)
            if r:
                search=r[0].split('&')[0]
                search=search.replace('q=', '').replace('+', ' ')
                print ('[+] '+ date + ' - Searched Google For: ' + search)
    
    # Duckduckgo
    for row in c:
        url = str(row[0])
        date = str(row[1])
        if 'duckduckgo' in url.lower():
            r = re.findall(r'wd=.*?\&', url)
            if r:
                search=r[0].split('&')[0]
                search=search.replace('wd=', '').replace('+', ' ')
                print ('[+] ' + date + ' - Searched For: ' + search)
    
    # Yandex
    for row in c:
        url = str(row[0])
        date = str(row[1])
        if 'yandex' in url.lower():
            r = re.findall(r'wd=.*?\&', url)
            if r:
                search=r[0].split('&')[0]
                search=search.replace('wd=', '').replace('+', ' ')
                print ('[+] ' + date + ' - Searched For: ' + search)

    # Startpage
    for row in c:
        url = str(row[0])
        date = str(row[1])
        if 'startpage' in url.lower():
            r = re.findall(r'wd=.*?\&', url)
            if r:
                search=r[0].split('&')[0]
                search=search.replace('wd=', '').replace('+', ' ')
                print ('[+] ' + date + ' - Searched For: ' + search)

    # Sougou
    for row in c:
        url = str(row[0])
        date = str(row[1])
        if 'sougou' in url.lower():
            r = re.findall(r'wd=.*?\&', url)
            if r:
                search=r[0].split('&')[0]
                search=search.replace('wd=', '').replace('+', ' ')
                print ('[+] ' + date + ' - Searched For: ' + search)

    # WikiPedia
    for row in c:
        url = str(row[0])
        date = str(row[1])
        if 'wikipedia' in url.lower():
            r = re.findall(r'wd=.*?\&', url)
            if r:
                search=r[0].split('&')[0]
                search=search.replace('wd=', '').replace('+', ' ')
                print ('[+] ' + date + ' - Searched For: ' + search)


# Parse the file places.sqlite and output the Bookmark Names and URLs
def print_bookmark(placesDB):
    conn = sqlite3.connect(placesDB)
    c = conn.cursor()

    print ('\n[*] --- Bookmarks --- ')
    # Google
    print ("-- Bookmark names contains keyword \"Google:\" --")
    c.execute("select title from moz_bookmarks")
    for row in c:
        title = str(row[0])
        if 'google' in title.lower():
            print ('[+] ' + title)
    print ("\n")
    
    print ("-- Bookmark URLs contains keyword \"google:\" --")
    c.execute("select * from moz_places")
    for row in c:
        url = str(row[1])
        if 'google' in url.lower():
            url = urllib.parse.unquote(url)
            print ('[+] ' + url)
    print ("\n")

    # Baidu or 百度
    print ("-- Bookmark names contains keyword \"Baidu:\" or \"百度\" --")
    c.execute("select title from moz_bookmarks")
    for row in c:
        title = str(row[0])
        if 'baidu' in title.lower():
            print ('[+] ' + title)
        if '百度' in title.lower():
            print ('[+] ' + title)
    print ("\n")
    
    print ("-- Bookmark URLs contains keyword \"baidu:\" --")
    c.execute("select * from moz_places")
    for row in c:
        url = str(row[1])
        if 'baidu' in url.lower():
            print ('[+] ' + url)
    print ("\n")

    # Bing
    print ("-- Bookmark names contains keyword \"Bing:\" or \"必应\" --")
    c.execute("select title from moz_bookmarks")
    for row in c:
        title = str(row[0])
        if 'bing' in title.lower():
            print ('[+] ' + title)
        if '必应' in title.lower():
            print ('[+] ' + title)
    print ("\n")
    
    print ("-- Bookmark URLs contains keyword \"bing:\" --")
    c.execute("select * from moz_places")
    for row in c:
        url = str(row[1])
        if 'bing' in url.lower():
            url = urllib.parse.unquote(url)
            print ('[+] ' + url)
    print ("\n")
    return


def main():
    parser = optparse.OptionParser("[*]Usage: firefoxParse.py -p <firefox profile path> ")
    parser.add_option('-p', dest='pathName', type='string', help='specify skype profile path')
    (options, args) = parser.parse_args()
    pathName = options.pathName
    if pathName == None:
        print (parser.usage)
        exit(0)
    elif os.path.isdir(pathName) == False:
        print ('[!] Path Does Not Exist: ' + pathName)
        exit(0)
    else:
        downloadDB = os.path.join(pathName, 'downloads.sqlite')
        if os.path.isfile(downloadDB):
            print_downloads(downloadDB)
        else:
            print ('[!] Downloads Db does not exist: '+downloadDB)

        cookiesDB = os.path.join(pathName, 'cookies.sqlite')
        if os.path.isfile(cookiesDB):
            pass
            print_cookies(cookiesDB)
        else:
            print ('[!] Cookies Db does not exist:' + cookiesDB)

        placesDB = os.path.join(pathName, 'places.sqlite')
        if os.path.isfile(placesDB):
            print_history(placesDB)
            print_search_engine(placesDB)
            print_bookmark(placesDB)
        else:
            print ('[!] PlacesDb does not exist: ' + placesDB)

if __name__ == '__main__':
    main()