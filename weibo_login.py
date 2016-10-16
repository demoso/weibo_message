#coding=utf8

# 2016-10-10
# @author Benjamin(zuojj.com@gmail.com)
# @home http://www.zuojj.com

import json
import base64
import requests

# @mthod login
# @description 模拟微博登录，并获取cookie
# @param username
# @parma password
# @return cookies
def login(username, password):
    username = base64.b64encode(username.encode('utf-8')).decode('utf-8')

    params = {
        "entry": "sso",
        "gateway": "1",
        "from": "null",
        "savestate": "30",
        "useticket": "0",
        "pagerefer": "",
        "vsnf": "1",
        "su": username,
        "service": "sso",
        "sp": password,
        "sr": "1440*900",
        "encoding": "UTF-8",
        "cdult": "3",
        "domain": "sina.com.cn",
        "prelt": "0",
        "returntype": "TEXT",
    }

    url = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'

    session = requests.Session()
    res = session.post(url, data = params)
    jsonStr = res.content.decode('utf-8')
    info = json.loads(jsonStr)

    if info["retcode"] == "0":
        print('login success')
        cookies = session.cookies.get_dict()
        cookies = [key + "=" + value for key, value in cookies.items()]
        cookies = "; ".join(cookies)
        print(cookies)
        return cookies
    else:
        print("login failed，the reason： %s" % info["reason"])
        return ""

# excute
login('cuew1987@163.com', 'xxxxx')











