import multiprocessing
from datetime import datetime
from ..log import LogPrint
from ..WebApiCall.WEBDriveDownURLTest import *
from ..SQL.ALLSQL import *


def DownURLTest(WorkList):
    for i in WorkList:
        sql = None
        Flag = None
        Id = i[0]
        URL = i[1]
        DownName = i[2]
        current_time = datetime.now()
        time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        if DownName == 'katfile':
            Flag = katfile(URL)
            if Flag is False:
                sql = f"UPDATE `AS_work_down_URL` SET  `url_state` = '9', `updata_time` = '{time}' WHERE `id` = {Id};"
            elif Flag is True:
                sql = f"UPDATE `AS_work_down_URL` SET  `url_state` = '1', `updata_time` = '{time}' WHERE `id` = {Id};"

        elif DownName == 'mexa' or DownName == 'mx-sh':
            Flag = mexa(URL)
            if Flag is False:
                sql = f"UPDATE `AS_work_down_URL` SET  `url_state` = '9', `updata_time` = '{time}' WHERE `id` = {Id};"
            elif Flag is True:
                sql = f"UPDATE `AS_work_down_URL` SET  `url_state` = '1', `updata_time` = '{time}' WHERE `id` = {Id};"

        elif DownName == 'rapidgator' or DownName == 'rg':
            Flag = rapidgator(URL)
            if Flag is False:
                sql = f"UPDATE `AS_work_down_URL` SET  `url_state` = '9', `updata_time` = '{time}' WHERE `id` = {Id};"
            elif Flag is True:
                sql = f"UPDATE `AS_work_down_URL` SET  `url_state` = '1', `updata_time` = '{time}' WHERE `id` = {Id};"

        elif DownName == 'rosefile':
            Flag = rosefile(URL)
            if Flag is False:
                sql = f"UPDATE `AS_work_down_URL` SET  `url_state` = '9', `updata_time` = '{time}' WHERE `id` = {Id};"
            elif Flag is True:
                sql = f"UPDATE `AS_work_down_URL` SET  `url_state` = '1', `updata_time` = '{time}' WHERE `id` = {Id};"

        elif DownName == 'ddownload':
            Flag = ddownload(URL)
            if Flag is False:
                sql = f"UPDATE `AS_work_down_URL` SET  `url_state` = '9', `updata_time` = '{time}' WHERE `id` = {Id};"
            elif Flag is True:
                sql = f"UPDATE `AS_work_down_URL` SET  `url_state` = '1', `updata_time` = '{time}' WHERE `id` = {Id};"

        elif DownName == 'fikper':
            Flag = fikper(URL)
            if Flag is False:
                sql = f"UPDATE `AS_work_down_URL` SET  `url_state` = '9', `updata_time` = '{time}' WHERE `id` = {Id};"
            elif Flag is True:
                sql = f"UPDATE `AS_work_down_URL` SET  `url_state` = '1', `updata_time` = '{time}' WHERE `id` = {Id};"

        F = UpdataAll(sql)
        if F is True:
            LogPrint(f"UPDATE AS_work_down_URL INFO URLStare:{Flag} ID:{Id} DownName:{DownName}")
        if F is False:
            LogPrint(f"UPDATE AS_work_down_URL ERROR URLStare:{Flag} ID:{Id} DownName")


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


def MultiProcessDownURLTest(processes, name):
    sql = f"SELECT id, work_dowm_url, dowm_web_name FROM AS_work_down_URL " \
          f"WHERE url_state = '0' and dowm_web_name IN {name}  limit 10000"
    WorkList = SelectAll(sql)
    # print(WorkList)
    if len(WorkList) == 0:
        print("已完成测试Down URL if Ture")
        return False
    chunks = split_list(WorkList, processes)
    pool = multiprocessing.Pool(processes=processes)
    pool.map(DownURLTest, chunks)
    pool.close()
    pool.join()
