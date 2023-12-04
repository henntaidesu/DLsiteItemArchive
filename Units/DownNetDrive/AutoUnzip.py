import os
import sys
import patoolib
from Units.NowTime import NowTime
from Units.SQL.ALLSQL import UpdataAll, SelectAll
from Units.ReadConf import ReadDownPath


def ExtractRAR(file_path, extract_path):
    # 使用日语编码 'cp932' 进行解压
    patoolib.extract_archive(file_path, outdir=extract_path, encoding='cp932')


def DeleteFile(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"The file {file_path} does not exist.")


def GetFileNames(folder_path):
    files = os.listdir(folder_path)
    files = [file for file in files if os.path.isfile(os.path.join(folder_path, file))]
    return files


def GetALLArchiveFiles(folder_path):
    archive_files = []
    # 遍历当前目录下的所有文件和文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            _, extension = os.path.splitext(file_path)

            # 判断文件是否为压缩文件（你可以根据需要添加其他压缩文件格式）
            if extension.lower() in ['.zip', '.rar', '.exe']:
                archive_files.append(file_path)
    # print(archive_files)
    return archive_files


def AutoDowmToUnzip(WorkId):
    while True:
        # WorkId = 'RJ01018336'
        FolderPath = ReadDownPath(WorkId)
        print(FolderPath)
        FileNameList = GetALLArchiveFiles(FolderPath)

        if len(FileNameList) == 0:
            Time = NowTime()
            sql = f"UPDATE `DLsite`.`works` SET `updata_time` = '{Time}', `work_state` = '-2' WHERE `work_id` = '{WorkId}';"
            UpdataAll(sql)
            return False
        FileName = FileNameList[0]
        if 'exe' in FileName:
            FileName = FileNameList[1]
        print(FileName)
        ExtractRAR(FileName, FolderPath)

        # 删除所有压缩文件
        for archive_file in FileNameList:
            DeleteFile(archive_file)


def AutoUnzip():
    sql = f"select work_id from works where work_state = '-1' limit 1"
    WorkId = SelectAll(sql)
    print(WorkId)
    WorkId = WorkId[0][0]
    print(WorkId)
    while True:
        # WorkId = 'RJ01018336'
        FolderPath = ReadDownPath(WorkId)
        print(FolderPath)
        FileNameList = GetALLArchiveFiles(FolderPath)

        if len(FileNameList) == 0:
            Time = NowTime()
            sql = f"UPDATE `DLsite`.`works` SET `updata_time` = '{Time}', `work_state` = '-2' WHERE `work_id` = '{WorkId}';"
            UpdataAll(sql)
            return False
        FileName = FileNameList[0]
        if 'exe' in FileName:
            FileName = FileNameList[1]
        print(FileName)
        ExtractRAR(FileName, FolderPath)

        # 删除所有压缩文件
        for archive_file in FileNameList:
            DeleteFile(archive_file)
