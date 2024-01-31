import sys

import requests
from src.ReadConf import ReadKatfileUser, WriteKatfileXFSS


def GETXFSS():
    User, PassWD = ReadKatfileUser()
    url = "https://katfile.com/"  # 替换为实际的API地址

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'op': 'login',
        'token': '',
        'rand': '',
        'redirect': '',
        'login': User,
        'password': PassWD,
        'submit': '',
    }
    response = requests.post(url, headers=headers, data=data, allow_redirects=False)
    try:
        data = response.headers
        SetCookie = data['Set-Cookie']
        SetCookie = str(SetCookie)
        StartIndex = SetCookie.find('xfss=')
        # 找到下一个分号的位置
        EndIndex = SetCookie.find(';', StartIndex)
        # 提取 'xfss' 的值
        XFSSValue = SetCookie[StartIndex + len('xfss='):EndIndex]
        print("已获取最新Cookie:")
        WriteKatfileXFSS(XFSSValue)
        return True
    except:
        print("Katfile账号或密码错误,注意密码连续错误三次以上，需要手动获取Cookie")
        sys.exit()
