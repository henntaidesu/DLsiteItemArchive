import multiprocessing
from datetime import datetime
from ..log import LogPrint
import requests
from ..SQL.ALLSQL import *


def TrimString(Str):
    if "'" in Str:
        Str = Str.replace("'", "\\'")
    if '"' in Str:
        Str = Str.replace('"', '\\"')
    return Str


def ReolveShortURL(short_url):
    short_url = str(short_url)
    url = "https://" + short_url
    # print(url)
    with requests.head(url, allow_redirects=True) as response:
        final_url = response.url

    return final_url


def ReDownTableShortURL(List):
    for i in List:
        Id = i[0]
        ShortURL = i[1]
        current_time = datetime.now()
        time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        LongURL = ReolveShortURL(ShortURL)
        if 'https' in LongURL[:8]:
            LongURL = LongURL[8:]
        else:
            LongURL = LongURL[7:]
        Name = LongURL.split('.')[0]
        LongURL = TrimString(LongURL)
        Name = TrimString(Name)
        if len(Name) > 12:
            Name = Name[:12]

        sql = f"UPDATE `DLsite`.`AS_work_down_URL` " \
              f"SET `work_dowm_url` = '{LongURL}', `url_state` = '0', `dowm_web_name` = '{Name}', " \
              f"`updata_time` = '{time}' WHERE `id` = {Id};"

        Flag = UpdataAll(sql)

        if Flag is True:
            LogPrint(f"Update Short INFO ID:{Id} New DownName:{Name}")
        if Flag is False:
            LogPrint(f"Update Short ERROR ID:{Id}")


def split_list(input_list, num_parts):
    avg = len(input_list) // num_parts
    remainder = len(input_list) % num_parts
    chunks = []
    current_idx = 0

    for i in range(num_parts):
        chunk_size = avg + 1 if i < remainder else avg
        chunks.append(input_list[current_idx:current_idx + chunk_size])
        current_idx += chunk_size

    return chunks


def MultiProcessReDownTableShortURL(processes, name):
    sql = f"SELECT id, work_dowm_url, dowm_web_name FROM AS_work_down_URL " \
          f"WHERE url_state = '0' and dowm_web_name in {name} "
    WorkList = SelectAll(sql)
    # print(WorkList)
    if len(WorkList) == 0:
        print("已完成转换Short URL")
        return False
    chunks = split_list(WorkList, processes)
    pool = multiprocessing.Pool(processes=processes)
    pool.map(ReDownTableShortURL, chunks)
    pool.close()
    pool.join()
