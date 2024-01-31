import os
import json


def NewFolder(FloderName):
    with open("Config.json", "r") as file:
        data = json.load(file)
        data = data[1]
        folder_path = data["DownPath"]
    folder_path = folder_path + FloderName
    # 使用os.makedirs()创建文件夹，如果文件夹已存在则不会引发错误
    os.makedirs(folder_path, exist_ok=True)
    print(f"Folder created at: {folder_path}")
    return folder_path


