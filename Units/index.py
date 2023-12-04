import time

from Units.QueryInformation.RjIdGenerate import RjIdGenerateNew
from Units.QueryInformation.CrawlDLWorks import ThreadCrawDLWorks
from Units.QueryInformation.CrawlWorkWEBInformation import ThreadCrawWEBInformation
from Units.Animei_Sharing.GainASWorkUpURL import MultiProcessASUpGroup
from Units.Animei_Sharing.GainWorkDownURL import MultiProcessASWorkDowmURL
from Units.DownNetDrive.URLTest import *
from Units.DownNetDrive.ResolveShortURL import MultiProcessReDownTableShortURL, ReDownTableShortURL
from Units.DownNetDrive.AutoDown.AutoDownKatfile import Autokatfile, QuerySpecificWork, AutoKatfileDown
from Units.Animei_Sharing.GetASUpGroupALLURL import GetASUpGroupALLURL


def Auto(Threads):
    DownName = "('katfile', 'mexa', 'mx-sh', 'rapidgator', 'rg', 'rosefile', 'ddownload')"
    ShortName = "('bit')"
    while True:
        ThreadCrawDLWorks(Threads)
        ThreadCrawWEBInformation(Threads)
        MultiProcessASUpGroup(Threads)
        MultiProcessASWorkDowmURL(Threads)
        MultiProcessReDownTableShortURL(Threads, ShortName)
        MultiProcessDownURLTest(Threads, DownName)
        time.sleep(7200)


def index():
    while True:
        print("\n")
        # print("1:从txt读取新works")
        # print("2:更新works数据")
        # print("3:更新DirectoryName数据")
        print("1:生成RJ数据")
        print("2:调用DL SELECT API更新works")
        print("3:更新information表")
        print("4:获取AS UPGroup")
        print("5:获取AS Down URL")
        print("6:测试Down URL if Ture")
        print("7:转换Short URL")

        flag = input()
        # flag = "b"
        Threads = 20
        print(F"进程数：{Threads}")

        # Threads = int(Threads)

        # if flag == "AAAAA":
        #     InsertWorksName()
        #
        # if flag == "2":
        #     UpWorksInf()
        #
        # if flag == "AAAA":
        #     ReDirectoryName()

        if flag == "qqq":
            RjIdGenerateNew()

        if flag == "2":
            ThreadCrawDLWorks(Threads)

        if flag == "3":
            ThreadCrawWEBInformation(Threads)

        if flag == '4':
            MultiProcessASUpGroup(Threads)

        if flag == "5":
            MultiProcessASWorkDowmURL(Threads)

        if flag == "6":
            DownName = "('katfile', 'mexa', 'mx-sh', 'rapidgator', 'rg', 'rosefile', 'ddownload')"
            while True:
                MultiProcessDownURLTest(Threads, DownName)

        if flag == "7":
            ShortName = "('bit')"
            while True:
                MultiProcessDownURLTest(Threads, ShortName)

        if flag == "a":
            while True:
                WorkId = input()
                QuerySpecificWork(WorkId)

        if flag == "b":
            while True:
                flag = AutoKatfileDown()
                if flag is False:
                    LogPrint("下载连接失效")
                if flag is True:
                    LogPrint("本作品已下载完")
        if flag == "q":
            GetASUpGroupALLURL()

        if flag == "auto":
            Auto(Threads)

























