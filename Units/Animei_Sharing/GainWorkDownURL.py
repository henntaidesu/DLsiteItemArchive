from datetime import datetime

from ..WebApiCall.AnimeSharingWorkDownURL import GETASWorkDowmURL
from ..SQL.ALLSQL import SelectAll, InsertALL, UpdataAll
import multiprocessing
from ..log import LogPrint
import sys


def TrimString(Str):
    if "'" in Str:
        Str = Str.replace("'", "\\'")
    if '"' in Str:
        Str = Str.replace('"', '\\"')
    return Str


def InsertDownURL(DownURLSet, Id, WorkId, URLState):
    unique_urls = list(set(DownURLSet))
    # print(unique_urls)
    for URL in unique_urls:
        current_time = datetime.now()
        time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        text = URL
        index = text.find(".")
        WebName = text[:index]
        # or WebName == "pixhost"
        if WebName[:3] == "www" or WebName[:2] == "ww" or WebName == "imagetwist":
            continue
        if WebName == "estpublic:guestpublic@bishoujo":
            # estpublic:guestpublic@bishoujo.moe:666
            WebName = "mikoconFTP"
        if "xt=urn" in WebName:
            WebName = "xt=urn"
        if len(WebName) > 12:
            WebName = WebName[:12]

        URL = TrimString(URL)
        WebName = TrimString(WebName)

        sql = f"INSERT INTO `AS_work_down_URL` (`group_table_id`, `work_dowm_url`, `url_state`,`dowm_web_name`, " \
              f"`updata_time`)VALUES ({Id}, '{URL}', '0', '{WebName}', '{time}');"
        InsertALL(sql)

    sql = f"UPDATE `AS_work_updata_group` SET  `url_state` = '{URLState}' WHERE `id` = {Id};"
    Flag = UpdataAll(sql)
    if Flag is True:
        LenData = len(unique_urls)  # 使用去重后的集合长度
        LogPrint(
            f"已查询到groupID - {Id} - 作品 - {WorkId} - 有{LenData}个下载连接，已更新AS_work_updata_group表 HTMLType:{URLState}")
    if Flag is False:
        LogPrint("ERROR")


def ASWorkDowmURL(WorkList):
    try:
        for List in WorkList:
            DownURLList = []
            Id = List[0]
            WorkId = List[1]
            GroupURL = List[2]
            try:
                Flag, DownURLSet = GETASWorkDowmURL(GroupURL)
                if DownURLSet:
                    for index in DownURLSet:
                        if index is None:
                            Flag = 4
                            continue
                        url = index[8:]
                        DownURLList.append(url)
                    InsertDownURL(DownURLList, Id, WorkId, Flag)
            except Exception as e:
                sql = f"UPDATE `AS_work_updata_group` SET  `url_state` = '8' WHERE `id` = {Id};"
                UpdataAll(sql)
                LogPrint(f"groupID - {Id} - 作品 - {WorkId} - 源HTML错误")
                print("发生错误:", str(e))
    except Exception as e:
        print("发生错误:", str(e))
        print("错误类型:", type(e).__name__)
        _, _, tb = sys.exc_info()
        print("发生错误的位置:", tb.tb_frame.f_code.co_filename, "第", tb.tb_lineno, "行")


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


def MultiProcessASWorkDowmURL(processes):
    sql = f"SELECT id, work_id, url FROM AS_work_updata_group WHERE url_state = '0' LIMIT 20000"
    WorkList = SelectAll(sql)
    # print(WorkList)
    if len(WorkList) == 0:
        print("已完成获取AS Down URL")
        return False
    chunks = split_list(WorkList, processes)
    pool = multiprocessing.Pool(processes=processes)
    pool.map(ASWorkDowmURL, chunks)
    pool.close()
    pool.join()
