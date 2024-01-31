import pymysql
import json


def ReadDBConf():
    with open("Config.json", "r") as file:
        data = json.load(file)
        data = data[0]
        host = data["host"]
        port = data["port"]
        user = data["user"]
        password = data["password"]
        database = data["database"]
    db = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
    return db


def ReadDownPath(FloderName):
    with open("Config.json", "r") as file:
        data = json.load(file)
        data = data[1]
        folder_path = data["DownPath"]
    folder_path = folder_path + FloderName
    return folder_path


def ReadKatfileCookie():
    with open("Config.json", "r") as file:
        data = json.load(file)
        data = data[2]
        katfileUser = data["User"]
        katfilePassWD = data["xfss"]
        Cookie = "login=" + katfileUser + ";" + "xfss=" + katfilePassWD
    return Cookie


def ReadKatfileUser():
    with open("Config.json", "r") as file:
        data = json.load(file)
        data = data[2]
        User = data["User"]
        PassWD = data["PassWD"]
    return User, PassWD


def ReadProxy():
    ProxyURL = None
    with open("Config.json", "r") as file:
        data = json.load(file)
        data = data[3]
        IFProxy = data["OpenProxy"]
        Add = data["Add"]
        Port = data["Port"]
        if IFProxy == "True":
            ProxyURL = "http://" + Add + ":" + Port
            return True, ProxyURL
        else:
            return False, ProxyURL


def WriteKatfileXFSS(xfss):
    with open("Config.json", "r") as file:
        data = json.load(file)
    data[2]["xfss"] = xfss
    with open("Config.json", "w") as file:
        json.dump(data, file)
