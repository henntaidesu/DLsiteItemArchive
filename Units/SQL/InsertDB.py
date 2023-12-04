from ..ReadConf import ReadDBConf
from Units.ReadWorksTxt import ReadWorksTxt
import sys
import time
from datetime import datetime


def InsertWorksName():
    try:
        WorksList = ReadWorksTxt()
        db = ReadDBConf()
        cursor = db.cursor()
        for i in WorksList:
            Temp = i
            if "'" in Temp:
                Temp = Temp.replace("'", "''")
            sql = f"INSERT INTO `DLsite`.`works`(`work_id`, `maker_id`, `work_name`, `age_category`, " \
                  f"`maker_name_kana`, `is_stock`) VALUES (NULL, NULL, '{Temp}', NULL, NULL, NULL);"
            cursor.execute(sql)
            db.commit()
            print(Temp)
        cursor.close()
        db.close()
    except Exception as e:
        print("错误信息:", str(e))
        print("错误类型:", type(e).__name__)
        _, _, tb = sys.exc_info()
        print("发生错误的位置:", tb.tb_frame.f_code.co_filename, "第", tb.tb_lineno, "行")


def InsertRjNumber(RjNunber):
    try:
        db = ReadDBConf()
        cursor = db.cursor()
        NowTime = time.time()
        # print(NowTime)
        datetime_obj = datetime.fromtimestamp(NowTime)
        formatted_date = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
        sql = f"INSERT INTO `DLsite`.`works`(`work_id`, `insert_time`) VALUES ('{RjNunber}','{formatted_date}');"
        # print(sql)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
    except Exception as e:
        print("错误信息:", str(e))
        print("错误类型:", type(e).__name__)
        _, _, tb = sys.exc_info()
        print("发生错误的位置:", tb.tb_frame.f_code.co_filename, "第", tb.tb_lineno, "行")


# def InsertWorksWEBinformation(sql):
#     try:
#         db = ReadDBConf()
#         cursor = db.cursor()
#         cursor.execute(sql)
#         db.commit()
#         cursor.close()
#         db.close()
#         return True
#     except Exception as e:
#         print("错误信息:", str(e))
#         print("错误类型:", type(e).__name__)
#         _, _, tb = sys.exc_info()
#         print("发生错误的位置:", tb.tb_frame.f_code.co_filename, "第", tb.tb_lineno, "行")
#         return False


def InsertALL(sql):
    try:
        db = ReadDBConf()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
        return True
    except Exception as e:
        print("错误信息:", str(e))
        print("错误类型:", type(e).__name__)
        _, _, tb = sys.exc_info()
        print("发生错误的位置:", tb.tb_frame.f_code.co_filename, "第", tb.tb_lineno, "行")
        print(sql)
        return False
