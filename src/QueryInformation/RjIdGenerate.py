from ..SQL.InsertDB import InsertRjNumber
from ..SQL.SelectDB import SelectWorksIdList
import time
import re


def RjIdGenerateNew():
    WorkList = SelectWorksIdList()
    Num = 1
    for i in WorkList:
        if i[0] == "RJ1000000":
            continue
        if len(i[0]) == 8:
            continue
        else:
            RjNum = str(i[0])
            RjNum = RjNum[-8:]
            RjNum = int(RjNum)
            if RjNum > Num:
                Num = RjNum

    RJ = "RJ"
    flag = 1
    while True:
        num_value = Num
        num_value += 1
        Num = num_value
        new_Num = f"{num_value:08d}"
        flag += 1
        if flag > 100000:
            break
        result = RJ + new_Num
        print(f"{result} Now: {flag}")
        InsertRjNumber(result)


def RjIdGenerateOLD():
    RJ = "RJ"
    Num = "899550"

    for i in range(1, 1000000):
        num_value = int(Num)
        num_value += 1
        Num = num_value
        new_Num = f"{num_value:06d}"
        if Num > 1000000:
            break
        result = RJ + new_Num
        print(result)
        InsertRjNumber(result)
