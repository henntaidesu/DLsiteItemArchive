from ..SQL.SelectDB import SelectWorksIDAndWorksTypeIsSOU
from ..WebApiCall.AnimeSharing import ASWorkURL
from ..SQL.ALLSQL import InsertALL, UpdataAll
from ..log import LogPrint
from Units.NowTime import NowTime
import multiprocessing
import sys


def ASWorkUpURL(WorksList):
    for i in WorksList:
        RjNumber = i[0]
        if len(RjNumber) < 9:
            LogPrint(RjNumber)
            Time = NowTime()
            sql = f"Update works set work_state = '98', updata_time = '{Time}' WHERE work_id = '{i[0]}' ;"
            UpdataAll(sql)
            continue

        Data = ASWorkURL(RjNumber)
        if Data:
            for j in Data:
                sql = f"INSERT INTO AS_work_updata_group(`work_id`, `group_name`, `url`, `url_state`) " \
                      f"VALUES ('{i[0]}', '{j[0]}', '{j[1]}', '0');"
                flag = InsertALL(sql)
                if flag is False:
                    # print(i[0] + "ERROR")
                    # print(sql)
                    LogPrint(i[0] + "ERROR")
                    LogPrint(sql)
                else:
                    # print(i[0] + "已获取AS上传组织URL数据")
                    LogPrint(i[0] + "已获取AS上传组织URL数据")
            Time = NowTime()
            sql = f"Update works set work_state = '15', updata_time = '{Time}' WHERE work_id = '{i[0]}' ;"
            flag = InsertALL(sql)
            if flag is False:
                # print(i[0] + "ERROR")
                # print(sql)
                LogPrint(i[0] + "ERROR")
                LogPrint(sql)
            else:
                # print(i[0] + "已更新works表")
                LogPrint(i[0] + "已更新works表")
        else:
            Time = NowTime()
            sql = f"UPDATE `works` SET `work_state` = '14', updata_time = '{Time}' WHERE `work_id` ='{i[0]}';"
            flag = InsertALL(sql)
            if flag is False:
                # print(i[0] + " ERROR")
                # print(sql)
                LogPrint(i[0] + " ERROR")
                LogPrint(sql)
            else:
                # print(i[0] + "无法从AS中获取数据")
                LogPrint(i[0] + "无法从AS中获取数据")


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


def MultiProcessASUpGroup(processes):
    WorkList = SelectWorksIDAndWorksTypeIsSOU()
    if len(WorkList) == 0:
        print("已完成获取AS UPGroup")
        return False
    chunks = split_list(WorkList, processes)
    pool = multiprocessing.Pool(processes=processes)
    pool.map(ASWorkUpURL, chunks)
    pool.close()
    pool.join()

# def split_list(input_list, num_parts):
#     avg = len(input_list) // num_parts
#     remainder = len(input_list) % num_parts
#     chunks = []
#     current_idx = 0
#
#     for i in range(num_parts):
#         chunk_size = avg + 1 if i < remainder else avg
#         chunks.append(input_list[current_idx:current_idx + chunk_size])
#         current_idx += chunk_size
#
#     return chunks
#
#
# def ThreadASUpGroup(Threads):
#     WorkList = SelectWorksIDAndWorksTypeIsSOU()
#     chunks = split_list(WorkList, Threads)
#
#     task_queue = queue.Queue()
#     threads = []
#
#     for i, chunk in enumerate(chunks):
#         thread = threading.Thread(target=ASWorkUpURL, args=(i, chunk))
#         threads.append(thread)
#
#     for thread in threads:
#         print(f"正在启动{thread}线程")
#         thread.start()
#
#     for thread in threads:
#         thread.join()
#
#     print("All Threads have completed")
