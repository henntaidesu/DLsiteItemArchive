import requests
import time
import json
from src.ReadConf import ReadProxy

def CallWorksAPI(term):
    OpenProxy, proxy_url = ReadProxy()
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }

    session = requests.Session()
    if OpenProxy is True:
        session.proxies.update(proxies)  # 将代理配置应用于该Session

    site = "adult-jp"
    touch = 0
    # 生成新的时间戳
    timestamp = int(time.time() * 1000)
    timestamp2 = timestamp + 2
    # 构建请求的 URL，包括新的时间戳
    url = f"https://www.dlsite.com/suggest/?term={term}&site={site}&time={timestamp}&touch={touch}&_={timestamp2}"
    response = session.get(url)
    # print(response.text)
    return response.text


def Transcode(term):
    List = CallWorksAPI(term)
    data = json.loads(List)
    # print(data)

    works = data.get('work', [])
    makers = data.get('maker', [])
    work_list = []
    maker_list = []

    for work in works:
        work_data = {
            'work_work_name': work.get('work_name', ''),
            'work_workno': work.get('workno', ''),
            'work_maker_name': work.get('maker_name', ''),
            'work_maker_id': work.get('maker_id', ''),
            'work_work_type': work.get('work_type', ''),
            'work_intro_s': work.get('intro_s', ''),
            'work_age_category': work.get('age_category', ''),
            'work_is_ana': work.get('is_ana', '')
        }
        work_list.append(work_data)

    if len(work_list) > 1:
        return "False"

    for maker in makers:
        maker_data = {
            'maker_maker_name': maker.get('maker_name', ''),
            'maker_workno': maker.get('workno', ''),
            'maker_maker_name_kana': maker.get('maker_name_kana', ''),
            'maker_make_id': maker.get('maker_id', ''),
            'maker_age_category': maker.get('age_category', ''),
            'maker_is_ana': maker.get('is_ana', '')
        }
        maker_list.append(maker_data)
    # print(work_list)
    # print(maker_list)
    return [work_list, maker_list]

