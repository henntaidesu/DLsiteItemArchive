from ..SQL.SelectDB import SelectWorksName
from ..SQL.OpenMysqlDB import ReadDBConf
from ..WebApiCall.GET import Transcode
from ..SQL.SelectDB import SelectMakerId
import sys
import time


def UpWorksInf():
    try:
        db = ReadDBConf()
        cursor = db.cursor()
        WorkList = SelectWorksName()
        for i in WorkList:

            Data = Transcode(i[0])
            # print(i[0])
            if not Data[0] or not Data[1]:
                print("接口无返回值")
                continue
            if Data == "False":
                print("接口存在重复数据")
                continue
            else:
                WorkName = Data[0][0]['work_work_name']
                if "'" in WorkName:
                    WorkName = WorkName.replace("'", "\\'")
                OldName = i[0]
                if "'" in OldName:
                    OldName = OldName.replace("'", "\\'")
                intro_s = Data[0][0]['work_intro_s']
                if "'" in intro_s:
                    intro_s = intro_s.replace("'", "\\'")
                sql = f"UPDATE `DLsite`.`works` SET " \
                      f"`work_id` = '{Data[0][0]['work_workno']}', " \
                      f"`maker_id` = '{Data[0][0]['work_maker_id']}', " \
                      f"`work_name` = '{WorkName}', " \
                      f"`age_category` = {Data[0][0]['work_age_category']}, " \
                      f"`maker_name_kana` = '{Data[1][0]['maker_maker_name_kana']}', " \
                      f"`intro_s` = '{intro_s}', " \
                      f"`is_stock` = 1 ,"\
                      f"`work_type` = '{Data[0][0]['work_work_type']}'"\
                      f"WHERE `work_name` = '{OldName}' ;"
                print(Data[0][0]['work_work_name'])
                # print(sql)
                cursor.execute(sql)
                db.commit()
                result = SelectMakerId(Data[0][0]['work_maker_id'])
                if result is True:
                    continue
                else:
                    TempMakerName = Data[0][0]['work_maker_name']
                    if "'" in TempMakerName:
                        TempMakerName = TempMakerName.replace("'", "\\'")
                    sql = f"INSERT INTO `DLsite`.`maker`" \
                          f"(`maker_id`, `maker_name`, `age_category`, `is_ana`) " \
                          f"VALUES " \
                          f"('{Data[0][0]['work_maker_id']}', " \
                          f"'{TempMakerName}'," \
                          f" '{Data[1][0]['maker_age_category']}', " \
                          f"'{Data[1][0]['maker_is_ana']}');"
                    # print(sql)
                    cursor.execute(sql)
                    db.commit()
        # time.sleep(3)
        cursor.close()
        db.close()
    except Exception as e:
        print("错误信息:", str(e))
        print("错误类型:", type(e).__name__)
        _, _, tb = sys.exc_info()
        print("发生错误的位置:", tb.tb_frame.f_code.co_filename, "第", tb.tb_lineno, "行")