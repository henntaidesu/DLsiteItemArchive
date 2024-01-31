import os
import shutil
import time
import sys
from ..SQL.SelectDB import SelectWorkName


def ReDirectoryName():
    try:
        directory_path = 'Y:\Works'
        items = os.listdir(directory_path)
        # print(items)
        # print(items[0])
        for i in items:
            if 'RJ' in [i][0]:
                # print([i][0])
                continue
            # print([i][0])
            WorkName = [i][0][-20:]
            WorkId = SelectWorkName(WorkName)
            # if WorkId and len(WorkId) >= 2:
            #     continue
            # print(WorkId)
            if WorkId is not False:
                old_folder_name = [i][0]
                new_folder_name = WorkId
                print(old_folder_name)
                print(new_folder_name)
                shutil.move(f'Y:\Works\{old_folder_name}', f'Y:\Works\{new_folder_name}')
                # time.sleep(3)

    except Exception as e:
        print("错误信息:", str(e))
        print("错误类型:", type(e).__name__)
        _, _, tb = sys.exc_info()
        print("发生错误的位置:", tb.tb_frame.f_code.co_filename, "第", tb.tb_lineno, "行")


