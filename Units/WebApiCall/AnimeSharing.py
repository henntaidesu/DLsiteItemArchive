import requests
from lxml import html
import urllib.parse
from Units.ReadConf import ReadProxy


def ASWorkURL(Work_id):
    try:
        # 设置代理
        OpenProxy, proxy_url = ReadProxy()
        proxies = {
            "http": proxy_url,
            "https": proxy_url,
        }
        session = requests.Session()  # 创建一个Session对象
        if OpenProxy is True:
            session.proxies.update(proxies)  # 将代理配置应用于该Session

        url = f"https://www.anime-sharing.com/search/7017202/?q={Work_id}&o=relevance"
        response = session.get(url)

        html_content = response.text
        tree = html.fromstring(html_content)
        title_elements = tree.cssselect('.block-body')
        GroupList = []
        # 遍历并处理找到的元素
        for title_element in title_elements:
            li_elements = title_element.findall('.//li')
            for li in li_elements:
                group = li.get('data-author')
                if group is None:
                    continue
                else:
                    a_element = li.find('.//a')
                    if a_element is not None:
                        url = a_element.get('href')
                        url = urllib.parse.unquote(url)
                        if 'https' in url[:8]:
                            url = url[8:]
                        else:
                            url = url[7:]
                        url = url[:-1]
                        groupStr = str(group)
                        groupStr = groupStr.lower()
                        groupStrLong = len(groupStr)
                        if groupStr == url[:groupStrLong]:
                            continue

                        GroupList.append((group, url))
        return GroupList
    except:
        print('sql')
