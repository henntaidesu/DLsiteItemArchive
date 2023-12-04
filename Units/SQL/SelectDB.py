from Units.ReadConf import ReadDBConf
import sys
import mysql.connector


def SelectWorksName():
    try:
        db = ReadDBConf()
        cursor = db.cursor()
        sql = f"SELECT work_name FROM `works` WHERE work_state IS NULL"
        cursor.execute(sql)
        WorkList = cursor.fetchall()
        cursor.close()
        db.close()
        return WorkList

    except Exception as e:
        print("错误信息:", str(e))
        print("错误类型:", type(e).__name__)
        _, _, tb = sys.exc_info()
        print("发生错误的位置:", tb.tb_frame.f_code.co_filename, "第", tb.tb_lineno, "行")


def SelectWorksRjNumber():
    try:
        db = ReadDBConf()
        cursor = db.cursor()
        sql = f"SELECT work_id FROM `works` WHERE  work_state = '1'  "
        cursor.execute(sql)
        WorkList = cursor.fetchall()
        cursor.close()
        db.close()
        return WorkList

    except Exception as e:
        print("错误信息:", str(e))
        print("错误类型:", type(e).__name__)
        _, _, tb = sys.exc_info()
        print("发生错误的位置:", tb.tb_frame.f_code.co_filename, "第", tb.tb_lineno, "行")


def SelectMakerId(MakeId):
    try:
        db = ReadDBConf()
        cursor = db.cursor()
        sql = f"SELECT maker_id FROM `maker` WHERE maker_id = '{MakeId}' "
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        db.close()

        if result:
            return True
        else:
            return False
    except Exception as e:
        print("错误信息:", str(e))
        print("错误类型:", type(e).__name__)
        _, _, tb = sys.exc_info()
        print("发生错误的位置:", tb.tb_frame.f_code.co_filename, "第", tb.tb_lineno, "行")


def SelectWorkName(DirectoryName):
    try:
        db = ReadDBConf()
        cursor = db.cursor()
        sql = f"SELECT work_id FROM `DLsite`.`works` WHERE `work_name` like '%{DirectoryName[0]}%'"
        # print(sql)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return False

    except Exception as e:
        print("错误信息:", str(e))
        print("错误类型:", type(e).__name__)
        _, _, tb = sys.exc_info()
        print("发生错误的位置:", tb.tb_frame.f_code.co_filename, "第", tb.tb_lineno, "行")


def SelectWorksRjNumberAndWorkType():
    try:
        db = ReadDBConf()
        cursor = db.cursor()
        sql = f"SELECT work_id, work_type FROM works WHERE work_state = '2' "
        # print(sql)
        cursor.execute(sql)
        WorkList = cursor.fetchall()
        cursor.close()
        db.close()
        return WorkList

    except Exception as e:
        print("错误信息:", str(e))
        print("错误类型:", type(e).__name__)
        _, _, tb = sys.exc_info()
        print("发生错误的位置:", tb.tb_frame.f_code.co_filename, "第", tb.tb_lineno, "行")


def SelectWorksNumber():
    try:
        db = ReadDBConf()
        cursor = db.cursor()
        sql = f"SELECT work_id FROM works WHERE work_name <> 'NULL' "
        cursor.execute(sql)
        WorkList = cursor.fetchall()
        cursor.close()
        db.close()
        return WorkList

    except Exception as e:
        print("错误信息:", str(e))
        print("错误类型:", type(e).__name__)
        _, _, tb = sys.exc_info()
        print("发生错误的位置:", tb.tb_frame.f_code.co_filename, "第", tb.tb_lineno, "行")


def SelectWorksIdList():
    try:
        db = ReadDBConf()
        cursor = db.cursor()
        sql = f"SELECT work_id FROM works"
        cursor.execute(sql)
        WorksIdList = cursor.fetchall()
        cursor.close()
        db.close()
        return WorksIdList

    except Exception as e:
        print("错误信息:", str(e))
        print("错误类型:", type(e).__name__)
        _, _, tb = sys.exc_info()
        print("发生错误的位置:", tb.tb_frame.f_code.co_filename, "第", tb.tb_lineno, "行")


def SelectWorksIDAndWorksTypeIsSOU():
    try:
        db = ReadDBConf()
        cursor = db.cursor()
        sql = f"SELECT work_id, work_type FROM works WHERE  work_state in {'7', '14'} LIMIT 5000"
        cursor.execute(sql)
        WorksList = cursor.fetchall()
        cursor.close()
        db.close()
        return WorksList

    except Exception as e:
        print("错误信息:", str(e))
        print("错误类型:", type(e).__name__)
        _, _, tb = sys.exc_info()
        print("发生错误的位置:", tb.tb_frame.f_code.co_filename, "第", tb.tb_lineno, "行")
