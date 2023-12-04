from ..ReadConf import ReadDBConf
from Units.ReadWorksTxt import ReadWorksTxt
import sys
import time
from datetime import datetime


def UpdateWorksTableIfInformationList(RjNunber, Flag):
    try:
        NowTime = time.time()
        datetime_obj = datetime.fromtimestamp(NowTime)
        formatted_date = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
        db = ReadDBConf()
        cursor = db.cursor()
        sql = f"UPDATE `DLsite`.`works` SET  `work_state` = '{Flag}' , `updata_time` = '{formatted_date}' " \
              f"WHERE `work_id` = '{RjNunber}';"
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
        return False


def UpdataWorksTableWorksStartList(start, RjNunber):
    try:
        db = ReadDBConf()
        cursor = db.cursor()
        sql = f"UPDATE `works` SET `work_state` = '{start}'  WHERE `work_id` = '{RjNunber}';"
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
        return False
