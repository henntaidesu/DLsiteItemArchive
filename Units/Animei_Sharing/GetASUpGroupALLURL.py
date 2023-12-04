import requests
from lxml import html
import urllib.parse
from Units.NowTime import NowTime
import sys
from Units.SQL.ALLSQL import InsertALL
from Units.log import LogPrint
import time


def GetASUpGroupALLURL():
    Name = 'Shine'
    page = 0
    try:
        while True:
            if page < 0:
                break
            page += 1
            print(page)
            url = f"https://www.anime-sharing.com/search/8706374/?page={page}&q=%2A&c[users]={Name}&o=date"
            print(url)
            response = requests.get(url)
            html_content = response.text
            tree = html.fromstring(html_content)
            title_elements = tree.cssselect('.block-body')
            GroupList = []
            # 遍历并处理找到的元素
            for title_element in title_elements:
                li_elements = title_element.findall('.//li')
                for li in li_elements:
                    group = li.get('data-author')
                    a_element = li.find('.//a')
                    if a_element is not None:
                        url = a_element.get('href')
                        url = urllib.parse.unquote(url)
                        url = url[9:]
                        url = url[:-1]
                        groupStr = str(group)
                        groupStr = groupStr.lower()
                        groupStrLong = len(groupStr)
                        if groupStr == url[:groupStrLong]:
                            continue
                        GroupList.append((group, url))

            for i in GroupList:
                groupName = i[0]
                Url = i[1]
                if groupName is None:
                    continue
                Time = NowTime()
                sql = f"INSERT INTO AS_group_UpWork( `group_name`, `url`, `insert_time`, `state`) " \
                      f"VALUES ('{groupName}', '{Url}', '{Time}', '1');"
                LogPrint(Url)
                InsertALL(sql)
            # time.sleep(5)

    except Exception as e:
        print("错误信息:", str(e))
        print("错误类型:", type(e).__name__)
        _, _, tb = sys.exc_info()
        print("发生错误的位置:", tb.tb_frame.f_code.co_filename, "第", tb.tb_lineno, "行")




