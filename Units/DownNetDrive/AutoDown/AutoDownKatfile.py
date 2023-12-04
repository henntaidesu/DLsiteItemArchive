import sys
from lxml import html
import time
import os
import requests
from tqdm import tqdm
from Units.SQL.ALLSQL import *
from Units.log import LogPrint
from Units.NewFolder import NewFolder
from datetime import datetime
from Units.NowTime import MiniNowTime, NowTime
from Units.ReadConf import ReadKatfileCookie, ReadProxy
from Units.WebApiCall.GETkatfileXFSS import GETXFSS
from Units.DownNetDrive.AutoUnzip import AutoDowmToUnzip


def QuerySpecificWork(WorkId):
    NowTime = time.time()
    datetime_obj = datetime.fromtimestamp(NowTime)
    formatted_date = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    sql = f"SELECT " \
          f"AS_work_updata_group.id, " \
          f"works_full_information.work_id, " \
          f"works.work_name " \
          f"FROM " \
          f"works_full_information, AS_work_updata_group,works  " \
          f"WHERE " \
          f"works_full_information.work_id = AS_work_updata_group.work_id  " \
          f"AND works.work_id = works_full_information.work_id " \
          f"AND works_full_information.work_id = '{WorkId}' " \
          f"AND AS_work_updata_group.group_name = 'Shine'  " \
          f"GROUP BY " \
          f"works.work_name, works_full_information.work_id, AS_work_updata_group.id "
    Work = SelectAll(sql)
    print(Work)
    Work = Work[0]
    Id = Work[0]
    WorkId = Work[1]
    WorkName = Work[2]
    sql2 = f"SELECT * FROM AS_work_down_URL WHERE group_table_id = {Id} AND dowm_web_name = 'katfile'"
    DownList = SelectAll(sql2)
    NewFolder(WorkId)
    if len(DownList) < 1:
        LogPrint("无数据")
    for i in DownList:
        url = i[2]
        url = 'https://' + url
        state = i[3]
        if state == 5:
            continue
        if len(DownList) <= 1:
            print(state + '   ' + url)
            continue
        if 'mp3' in url:
            continue
        print(state + '   ' + url)

    sql2 = f"update works set work_state = '-1' , `updata_time` = '{formatted_date}' where work_id = '{WorkId}'"
    flag = UpdataAll(sql2)


def Autokatfile():
    Id = None
    WorkId = None
    WorkName = None
    try:
        GN = 'Shine'
        maker_id = "RG49556"
        LimitData = '2022-01-01'
        sql1 = f"SELECT AS_work_updata_group.id ,works_full_information.work_id, works.work_name " \
               f"FROM works_full_information, AS_work_updata_group, works " \
               f"WHERE works_full_information.work_id = AS_work_updata_group.work_id " \
               f"AND works.work_id = works_full_information.work_id " \
               f"AND works_full_information.Release_data > '{LimitData}' " \
               f"AND works_full_information.work_type = 'SOU' " \
               f"AND works_full_information.tag like '%耳かき%' " \
               f"AND AS_work_updata_group.group_name = '{GN}' " \
               f"AND AS_work_updata_group.url_state IN ('1', '2', '3', '4') " \
               f"AND works.work_state = '15'  " \
               f"GROUP BY works.work_name,  works_full_information.work_id, AS_work_updata_group.id " \
               f"Limit 1"
        Work = SelectAll(sql1)
        Work = Work[0]
        Id = Work[0]
        WorkId = Work[1]
        WorkName = Work[2]
        sql2 = f"SELECT * FROM AS_work_down_URL WHERE group_table_id = {Id} AND dowm_web_name = 'katfile'"
        DownList = SelectAll(sql2)
        DownurlList = []
        IDList = []
        UrlIdLsit = []
        if len(DownList) < 1:
            LogPrint("无数据")
        if len(DownList) == 1:
            DownListTemp = DownList[0]
            UrlId = DownListTemp[0]
            UrlIdLsit.append(UrlId)
            Downurl = DownListTemp[2]
            DownurlList.append(Downurl)
            state = DownListTemp[3]
            if state == '9':
                Time = NowTime()
                sql = f"update works set work_state = '22',`updata_time`= '{Time}' where work_id = '{WorkId}'"
                UpdataAll(sql)
                LogPrint('AS上有下载连接已失效')
                return False, Downurl, WorkId
            return UrlIdLsit, DownurlList, WorkId

        for i in DownList:
            UrlId = i[0]
            Downurl = i[2]
            state = i[3]
            if 'mp3' in Downurl:
                continue
            if state == "5":
                continue
            if state == "9":
                Time = MiniNowTime()
                sql2 = f"update works set work_state = '23',`updata_time`='{Time}' where work_id = '{WorkId}'"
                UpdataAll(sql2)
                LogPrint('Katfile的Shine上有部分下载连接已失效')
                print(state + '   ' + Downurl)
                return False, Downurl, WorkId
            DownurlList.append(Downurl)
            IDList.append(UrlId)
            print(state + '   ' + Downurl)
            if len(DownList) == 0:
                Time = MiniNowTime()
                sql = f"UPDATE `works`SET `updata_time` = '{Time}', `work_state` = '-1' WHERE `work_id` = '{WorkId}';"
                UpdataAll(sql)
                LogPrint(WorkId + "已完成下载")

                return True, Downurl, WorkId
        return IDList, DownurlList, WorkId

    except:
        LogPrint(f'{Id}, {WorkId}, {WorkName}')



def AutoKatfileDown():
    try:
        # 设置代理
        OpenProxy, proxy_url = ReadProxy()
        proxies = {
            "http": proxy_url,
            "https": proxy_url,
        }
        Cookie = ReadKatfileCookie()
        headers = {
            'Cookie': Cookie,
        }
        UrlIdList, DownurlList, WorkId = Autokatfile()
        if UrlIdList is False:
            return False
        if UrlIdList is True:
            return True
        flag = 0
        flag = int(flag)
        for i in DownurlList:
            time.sleep(3)
            UrlId = UrlIdList[flag]
            flag += 1
            OriginalURL = i
            url = 'https://' + OriginalURL
            session = requests.Session()  # 创建一个Session对象
            if OpenProxy is True:
                session.proxies.update(proxies)  # 将代理配置应用于该Session
                
            response = session.get(url, headers=headers, allow_redirects=False)  # allow_redirects=False不进行重定向

            print("Redirected Code:", response.status_code)
            if response.status_code == 200:
                WebData = response.text
                if 'Login' in WebData:
                    print("Cookie错误 开始自动获取Cookie")
                    Flag = GETXFSS()
                    if Flag is True:
                        print("已获取最新Cookie将开始自动下载")
                        AutoKatfileDown()

                elif 'reCAPTCHA' in WebData:
                    print("请确保改账户为Premium")
                    print("或者未开启Direct downloads，请前往个人中心开启")
                    print("https://katfile.com/?op=my_account")
                    sys.exit()
            DownPath = NewFolder(WorkId)
            os.makedirs(DownPath, exist_ok=True)  # 确保下载路径存在
            if response.is_redirect:
                # 获取重定向后的 URL
                redirected_url = response.headers.get('location')
                print(f'Redirected URL: {redirected_url}')

                URLstring = str(redirected_url)
                last_slash_index = URLstring.rfind('/')
                filename = URLstring[last_slash_index + 1:]
                print("filename:" + filename)

                # 检查本地文件是否存在
                file_path = os.path.join(DownPath, filename)
                if os.path.exists(file_path):
                    # 如果文件已存在，获取已下载的文件大小
                    resume_header = {'Range': 'bytes=%d-' % os.path.getsize(file_path)}
                    response = session.get(redirected_url, headers=resume_header, stream=True)
                else:
                    response = session.get(redirected_url, stream=True)

                download_complete = False
                while not download_complete:

                    try:
                        if response.status_code == 416:
                            print(response.status_code)
                            print("检查代理设置或删除最近一个下载的文件")
                            sys.exit()
                        if response.status_code == 200 or response.status_code == 206:  # 206表示部分内容
                            total_size = int(response.headers.get('content-length', 0))
                            block_size = 1024  # 1 KB
                            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

                            with open(file_path, 'ab') as file:  # 使用追加模式打开文件
                                for data in response.iter_content(block_size):
                                    progress_bar.update(len(data))
                                    file.write(data)

                            progress_bar.close()
                            Time = MiniNowTime()
                            sql = f"UPDATE `AS_work_down_URL` SET  `url_state` = '5' ,`updata_time` = '{Time}' WHERE " \
                                  f"`id` = '{UrlId}';"
                            UpdataAll(sql)
                            download_complete = True  # 下载完成

                        else:
                            # 处理非200和206状态码，可以根据需要进行处理
                            print(f"Error: {response.status_code}")
                            time.sleep(3)

                    except requests.exceptions.RequestException as e:
                        print(f"网络错误: {e}")
                        time.sleep(3)
                        AutoKatfileDown()
            else:
                # 处理非200状态码，可以根据需要进行处理
                print(f"处理非200状态码，Error: {response.status_code}")

        Time = MiniNowTime()
        sql = f"UPDATE `works`SET `updata_time` = '{Time}', `work_state` = '-1' WHERE `work_id` = '{WorkId}';"
        UpdataAll(sql)
        LogPrint(WorkId + "已完成下载")
        AutoDowmToUnzip(WorkId)
        LogPrint(WorkId + "已完成解压")

    except Exception as e:
        print("错误信息:", str(e))
        print("错误类型:", type(e).__name__)
        _, _, tb = sys.exc_info()
        print("发生错误的位置:", tb.tb_frame.f_code.co_filename, "第", tb.tb_lineno, "行")
