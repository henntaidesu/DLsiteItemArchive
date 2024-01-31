import time
from datetime import datetime

from .SQL.ALLSQL import SelectAll, UpdataAll


def a():
    sql = f"SELECT `1` FROM test"
    Data = SelectAll(sql)
    return Data


def b():
    Data = a()
    for i in Data:
        sql = f"UPDATE works SET work_state = '-9' WHERE work_id = '{i[0]}'; "
        print(sql)
        # UpdataAll(sql)


def ReTableWorkListWork_state(workid, State):
    NowTime = time.time()
    datetime_obj = datetime.fromtimestamp(NowTime)
    formatted_date = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    sql = f"UPDATE works set updata_time = '{formatted_date}' , work_state = '{State}' WHERE workid = '{workid}'; "
    UpdataAll(sql)
