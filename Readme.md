# 浏览器记录解析脚本

## 主要功能

1. 解析浏览器用户目录，支持 `Firefox` 类和 `Chromium` 类的浏览器
2. 自动解析 `Cookies` 信息
3. 解析浏览器历史记录
4. 解析用户搜索记录，支持百度、Google、Bing、Yandex、Duckduckgo 等
5. 解析书签
6. 可指定自定义关键词字典进行额外分析

## 使用方式

通过 `python ./main.py -h` 命令获得帮助：

```bash
Usage: main.py -b <Browser version (Firefox or Chromium)> -p <Browser profile path> -k <Custom keyword dictionary file>

Options:
  -h, --help          show this help message and exit
  -b BROWSER_VERSION  Specify browser version (Firefox or Chromium)
  -p PATH_NAME        Specify Browser profile path
  -k CUSTOM_KEYWORD   Specify custom keyword dictionary file
```

通过参数 `-p` 指定 Firefox 的 `Profile` 目录，通常在用户主目录下的 `\AppData\Roaming\Mozilla\Firefox\Profiles\` 里面，选取需要分析的即可；

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

# Browser Record Parsing Script

## Main Function

1. Parsing the user's browser profile directory, support `Firefox` and `Chromium` based browsers.
2. Parsing the user cookies automatically.
3. Parsing the user's browsing history.
4. Parsing the user's searching history, support Baidu, Google, Bing, Yandex, Duckduckgo, Startpage.
5. Parsing the bookmark.
6. Support analyzing the bookmark using customized dictionary file.

## Usage

Get help using `python ./main.py -h`:

```bash
Usage: [*] Usage: firefoxParse.py -p <firefox profile path> -c <Custom keyword dictionary>

Options:
  -h, --help         show this help message and exit
  -p PATH_NAME       Specify Firefox profile path
  -k CUSTOM_KEYWORD  Specify custom keyword dictionary file

```

Specify Firefox's `Profile` directory by parameter `-p`, usually in `\AppData\Roaming\Mozilla\Firefox\Profiles` under the user's home directory.

Specify browser version by parameter `-b`, and the options can be `-b Firefox` or `-b Chromium`. For example, browsers such as `Firefox`, `Tor Browser`, `Firefox-ESR`, which are using `Gecko` Kernel should be specified as `Firefox`, and browsers such as `Chromium`, `Google Chrome`, `Microsoft Edge` which are using `Chromium` Kernel should be specified as `Chromium` :

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
