from src.ReadConf import ReadDBConf
from src.log import LogPrint
import sys
import html


def HtmlTrim(Str):
    escaped_html = html.escape(Str)
    return escaped_html


def ReHtmlTrim(Str):
    original_html = html.unescape(Str)
    return original_html


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
        if "timed out" in str(e):
            LogPrint("连接数据库超时")
        print(sql)
        return False


def InsertALLList(sql):
    try:
        db = ReadDBConf()
        cursor = db.cursor()
        for i in sql:
            cursor.execute(sql[i])
            db.commit()
            cursor.close()
        db.close()
        return True
    except Exception as e:
        print("错误信息:", str(e))
        print("错误类型:", type(e).__name__)
        _, _, tb = sys.exc_info()
        print("发生错误的位置:", tb.tb_frame.f_code.co_filename, "第", tb.tb_lineno, "行")
        if "timed out" in str(e):
            LogPrint("连接数据库超时")
        print(sql)
        return False


def UpdataAll(sql):
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
        if "timed out" in str(e):
            LogPrint("连接数据库超时")
        print(sql)
        return False


def SelectAll(sql):
    try:
        db = ReadDBConf()
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return result
    except Exception as e:
        print("错误信息:", str(e))
        print("错误类型:", type(e).__name__)
        _, _, tb = sys.exc_info()
        print("发生错误的位置:", tb.tb_frame.f_code.co_filename, "第", tb.tb_lineno, "行")
        if "timed out" in str(e):
            LogPrint("连接数据库超时")
        print(sql)


