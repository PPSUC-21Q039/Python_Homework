# Firefox 浏览器记录解析脚本

## 主要功能

1. 解析 Firefox 目录，自动解析 `Cookies` 信息
2. 解析浏览器历史记录
3. 解析用户搜索记录，支持百度、Google、Bing、Yandex、Duckduckgo、Startpage 等
4. 解析书签
5. 可指定自定义关键词字典进行额外分析

## 使用方式

通过 `python ./main.py -h` 命令获得帮助：

```bash
Usage: [*] Usage: firefoxParse.py -p <firefox profile path> -c <Custom keyword dictionary>

Options:
  -h, --help          show this help message and exit
  -b BROWSER_VERSION  Specify browser version (Firefox or Chromium)
  -p PATH_NAME        Specify Browser profile path
  -k CUSTOM_KEYWORD   Specify custom keyword dictionary file
```

通过参数 `-p` 指定 Firefox 的 `Profile` 目录，通常在用户主目录下的 `\AppData\Roaming\Mozilla\Firefox\Profiles\` 里面，选取其中一个即可，只指定参数 `-p` 时则进行自动分析；

通过参数 `-b` 指定浏览器类型，可选项为 `-b Firefox` 或 `-b Chromium` , 其中 `Firefox`、`Tor Browser`、`Firefox-ESR` 等使用 `Gecko` 内核的属于 `Firefox ` 类型，`Chromium `、`Google Chrome `、`Microsoft Edge `等使用 `Chromium`内核的属于 `Chromium` 类型：

```bash
> python .\main.py -p "C:\Users\***\AppData\Roaming\Mozilla\Firefox\Profiles\***.default-esr" -b Firefox
```

指定参数 `-k` 可指定关键词字典文件进行自定义分析：

```bash
> python .\main.py -p C:\Users\***\AppData\Roaming\Mozilla\Firefox\Profiles\***.default-esr -b Firefox -k ./keyword.txt 
```

其中，`keyword.txt` (也可以是别的文件名) 的内容按照行进行分隔，一行只保留一个关键词。

如果输出过多，可重定向到某个本地文件，如：

```bash
> python .\main.py -p C:\Users\***\AppData\Roaming\Mozilla\Firefox\Profiles\***.default-esr -b Firefox -k ./keyword.txt > ./output.txt
```

---

# Firefox Browsing Record Parsing Script

## Main Function

1. Parsing the Firefox user profile directory and parsing the user cookies automatically.
2. Parsing the user's browsing history.
3. Parsing the user's searching history, support Baidu, Google, Bing, Yandex, Duckduckgo, Startpage.
4. Parsing the bookmark.
5. Support analyzing the bookmark using customized dictionary file.

## Usage

Get help using `python ./main.py -h`:

```bash
Usage: [*] Usage: firefoxParse.py -p <firefox profile path> -c <Custom keyword dictionary>

Options:
  -h, --help         show this help message and exit
  -p PATH_NAME       Specify Firefox profile path
  -k CUSTOM_KEYWORD  Specify custom keyword dictionary file

```

Specify Firefox's `Profile` directory by parameter `-p`, usually in `\AppData\Roaming\Mozilla\Firefox\Profiles` under the user's home directory. The script will automatically analyze when only parameter `-p` is specified;

Specify browser version by parameter `-b`, and the options can be `-b Firefox` or `-b Chromium`. For example, browsers such as `Firefox`, `Tor Browser`, `Firefox-ESR`, which are using `Gecko` Kernel should be specified as `Firefox`, and browsers such as `Chromium`, `Google Chrome`, `Microsoft Edge` which are using `Chromium` Kernel should be specified as `Chromium`:

```bash
> python .\main.py -p "C:\Users\***\AppData\Roaming\Mozilla\Firefox\Profiles\***.default-esr" -b Firefox
```

When parameter `-k` is specified, a customized keyword dictionary file can be used for custom analytics:

```bash
> python .\main.py -p C:\Users\***\AppData\Roaming\Mozilla\Firefox\Profiles\***.default-esr -b Firefox -k ./keyword.txt 
```

The contents in the file `Keyword.txt` (Can be other filenames) should be separated by Return.

If there are too many outputs, you can redirect to a certain file:

```bash
> python .\main.py -p C:\Users\***\AppData\Roaming\Mozilla\Firefox\Profiles\***.default-esr -b Firefox -k ./keyword.txt > ./output.txt
```
