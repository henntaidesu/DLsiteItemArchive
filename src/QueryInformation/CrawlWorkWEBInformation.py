from ..WebApiCall.CallWorksWebUI import CallWorksWebUI
from ..SQL.SelectDB import SelectWorksRjNumberAndWorkType
from ..SQL.InsertDB import InsertALL
from ..SQL.UpdateDB import UpdateWorksTableIfInformationList
from ..log import LogPrint
import multiprocessing
import threading
from queue import Queue
import sys

def CrawlWorkWEBInformation(WorksList):
    for i in WorksList:
        RJNumber = i[0]
        WorkType = i[1]
        IfRelease, sql = CallWorksWebUI(RJNumber, WorkType)
        if sql == "ERROR":
            UpdateWorksTableIfInformationList(RJNumber, 10)
            # print(f"{RJNumber} この作品は現在販売されていません")
            LogPrint(f"{RJNumber} - この作品は現在販売されていません")
            continue
        # print(sql)
        if IfRelease is False:
            Flag1 = InsertALL(sql)
            if Flag1 is True:
                UpdateWorksTableIfInformationList(RJNumber, 7)
                # print(f"更新表works,information中作品{RJNumber}成功")
                LogPrint(f"更新表works,information中作品 - {RJNumber} - 成功")
            else:
                UpdateWorksTableIfInformationList(RJNumber, 8)
                # print(f"{RJNumber}:ERROR")
                LogPrint(f"{RJNumber}:ERROR")
        if IfRelease is True:
            Flag1 = InsertALL(sql)
            if Flag1 is True:
                UpdateWorksTableIfInformationList(RJNumber, 9)
                # print(f"更新表works,information中作品{RJNumber}成功，作品处于待发售状态")
                LogPrint(f"更新表works,information中作品 - {RJNumber} - 成功，作品处于待发售状态")
            else:
                UpdateWorksTableIfInformationList(RJNumber, 8)
                # print(f"{RJNumber}:更新")
                LogPrint(f"{RJNumber}:更新")


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


def ThreadCrawWEBInformation(processes):
    WorkList = SelectWorksRjNumberAndWorkType()
    chunks = split_list(WorkList, processes)
    if len(WorkList) == 0:
        print("已完成更新information表")
        return False
    else:
        pool = multiprocessing.Pool(processes=processes)
        pool.map(CrawlWorkWEBInformation, chunks)
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
# def ThreadCrawWEBInformation(Threads):
#     RJList = SelectWorksRjNumberAndWorkType()
#     chunks = split_list(RJList, Threads)
#
#     task_queue = Queue()
#     threads = []
#
#     for i, chunk in enumerate(chunks):
#         thread = threading.Thread(target=CrawlWorkWEBInformation, args=(chunk,))
#         threads.append(thread)
#
#     for thread in threads:
#         print(f"正在启动 {thread} 线程")
#         thread.start()
#
#     for thread in threads:
#         thread.join()
#
#     print("All Threads have completed")


# def TestCrawlWorkWEBInformation():
#     RJNumber = "RJ01025454"
#     WorkType = "ADV"
#     IfRelease, sql = CallWorksWebUI(RJNumber, WorkType)
#     print(IfRelease, "\n\n\n")
#     print(sql)
#     # Flag = InsertWorksWEBinformation(sql)
#     # if Flag is True:
#     #     print(RJNumber, "已更新数据")
