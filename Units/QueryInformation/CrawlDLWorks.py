import gc
import threading
from queue import Queue
from ..WebApiCall.GET import Transcode
from ..SQL.SelectDB import SelectMakerId, SelectWorksRjNumber
import sys
from Units.NowTime import NowTime
import multiprocessing
from ..log import LogPrint
from ..SQL.ALLSQL import InsertALL, SelectAll


def CrawDLWorks(chunk):
    try:
        for i in chunk:
            formatted_date = NowTime()
            gc.collect()
            Data = Transcode(i[0])
            # if len(i[0]) < 9:
            #     LogPrint(i[0] + "旧数据")
            #     sql = f"UPDATE `works` SET  `work_state` = '99', `updata_time` = '{formatted_date}' " \
            #           f" WHERE `work_id` = '{i[0]}'"
            #     InsertALL(sql)
            #     continue
            #
            # if len(i[0]) > 9:
            #     LogPrint(i[0] + "New")
            #     continue
            if not Data[0] or not Data[1]:
                sql = f"UPDATE `works` SET  `work_state` = '1', `updata_time` = '{formatted_date}' " \
                      f" WHERE `work_id` = '{i[0]}'"
                InsertALL(sql)
                LogPrint(f"{i[0]} - 接口无返回值")
                continue
            if Data == "False":
                LogPrint(f"{i[0]} - 接口存在重复数据")
                sql = f"UPDATE `works` SET  `work_state` = '4', `updata_time` = '{formatted_date}' " \
                      f" WHERE `work_id` = '{i[0]}'"
                InsertALL(sql)
                continue
            else:
                maker_id = Data[0][0]['work_maker_id']
                if "'" in maker_id:
                    maker_id = maker_id.replace("'", "\\'")

                WorkName = Data[0][0]['work_work_name']
                if "'" in WorkName:
                    WorkName = WorkName.replace("'", "\\'")

                try:
                    maker_name_kana = Data[1][0]['maker_maker_name_kana']
                    if "'" in maker_name_kana:
                        maker_name_kana = maker_name_kana.replace("'", "\\'")
                except:
                    maker_name_kana = "NULL"
                intro_s = Data[0][0]['work_intro_s']
                if "'" in intro_s:
                    intro_s = intro_s.replace("'", "\\'")

                work_type = Data[0][0]['work_work_type']
                if "'" in work_type:
                    work_type = work_type.replace("'", "\\'")

                work_workno = Data[0][0]['work_workno']

                if len(WorkName) > 128:
                    WorkName = WorkName[:128]

                sql1 = f"UPDATE `works` SET " \
                       f"`maker_id` = '{maker_id}', " \
                       f"`work_name` = '{WorkName}', " \
                       f"`age_category` = {Data[0][0]['work_age_category']}, " \
                       f"`maker_name_kana` = '{maker_name_kana}', " \
                       f"`intro_s` = '{intro_s}', " \
                       f"`work_type` = '{work_type}', `updata_time` = '{formatted_date}', `work_state` = '2'  " \
                       f"WHERE `work_id` = '{i[0]}' ;"
                # print(work_workno, "项目作品名称", Data[0][0]['work_work_name'])
                LogPrint(work_workno + " - 项目作品名称 - " + Data[0][0]['work_work_name'])
                # print(sql1)
                InsertALL(sql1)
                result = SelectMakerId(Data[0][0]['work_maker_id'])
                if result is True:
                    continue
                else:
                    TempMakerName = Data[0][0]['work_maker_name']
                    if "'" in TempMakerName:
                        TempMakerName = TempMakerName.replace("'", "\\'")
                    sql2 = f"INSERT INTO `maker`" \
                           f"(`maker_id`, `maker_name`, `age_category`, `is_ana`) " \
                           f"VALUES " \
                           f"('{Data[0][0]['work_maker_id']}', " \
                           f"'{TempMakerName}'," \
                           f" '{Data[1][0]['maker_age_category']}', " \
                           f"'{Data[1][0]['maker_is_ana']}');"
                    # print(sql)
                    InsertALL(sql2)

        # random_float = random.uniform(0, 2)
        # print(random_float)
        # time.sleep(random_float)
    except Exception as e:
        print("错误信息:", str(e))
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


def ThreadCrawDLWorks(processes):
    time = NowTime()
    sql = "SELECT work_id FROM `works` WHERE  work_state = '1' and updata_time < '2023-11-30 23:32:00'"
    WorkList = SelectAll(sql)
    if len(WorkList) == 0:
        print("已完成调用DL SELECT API更新works")
        return False
    chunks = split_list(WorkList, processes)
    pool = multiprocessing.Pool(processes=processes)
    pool.map(CrawDLWorks, chunks)
    pool.close()
    pool.join()

