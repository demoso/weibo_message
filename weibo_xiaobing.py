#coding=utf8

import time
import json
import base64
import os
import sqlite3
import requests
from win32.win32crypt import CryptUnprotectData

# @author Benjamin(zuojj.com@gmail.com)

def login(username, password):
    username = base64.b64encode(username.encode('utf-8')).decode('utf-8')

    postData = {
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
    loginURL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    session = requests.Session()
    res = session.post(loginURL, data = postData)
    jsonStr = res.content.decode('gbk')
    info = json.loads(jsonStr)
    if info["retcode"] == "0":
        print('login success')
    else:
        print("login failed，the reason： %s" % info["reason"])

#login('cuew1987@163.com', 'xxxx')

def getPrivateMsgCookie(host='.weibo.com'):
    cookiepath = os.environ['LOCALAPPDATA']+r"\Google\Chrome\User Data\Default\Cookies"

    sql="select host_key,name,encrypted_value from cookies where host_key='%s'" % host
    with sqlite3.connect(cookiepath) as conn:
        cu = conn.cursor()
        privateMsgCookie = {
            name: CryptUnprotectData(encrypted_value)[1].decode() for host_key,name,encrypted_value in cu.execute(sql).fetchall()
            }

        private = "";
        for key in privateMsgCookie:
            private += key + "=" + privateMsgCookie[key] + ";"

    print(private + "\n")
    return private

cookie = getPrivateMsgCookie()

def postMsg(msg):
    url = "http://weibo.com/aj/message/add?"
    data = "ajwvr=6&__rnd="+ str(int(time.time())) +"&location=msgdialog&module=msgissue&style_id=1&text=" + msg + "&uid=5175429989&tovfids=&fids=&el=[object HTMLDivElement]&_t=0"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,ko;q=0.6,en;q=0.4,zh-TW;q=0.2,fr;q=0.2",
        "Connection": "keep-alive",
        "Content-Length": str(len(msg)),
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": cookie,
        "Host": "weibo.com",
        "Origin": "http://weibo.com",
        "Referer": "http://weibo.com/message/history?uid=5175429989&name=%E5%B0%8F%E5%86%B0",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    r = requests.post(url, headers=headers, data=data)
    jsonStr = r.content.decode('utf-8')
    info = json.loads(jsonStr)
    return info

def getMsg(msg):
    url = "http://m.weibo.cn/msg/messages?uid=5175429989&page=1"
    get_headers = {
        "Host": "m.weibo.cn",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": str(1),
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "http://m.weibo.cn/msg/chat?uid=5175429989",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8,ko;q=0.6,en;q=0.4,zh-TW;q=0.2,fr;q=0.2",
        "Cookie": cookie
    }

    return repeatGet(url, get_headers, msg)

def repeatGet(url, get_headers, msg):
    response = requests.get(url, headers=get_headers)
    result = ""
    if response:
        obj = json.loads(response.text)

        if "data" in obj:
            result = obj['data'][0]['text']
            #print(result)
            #print(result == msg)
            if(result == msg):
                result = repeatGet(url, get_headers, msg)

            if result == "分享语音":
                result = result + str(obj['data'][0]['attachment'][0]['filename'].encode('utf-8'))
    return result

if __name__ == "__main__":
    while True:
        msg = input('say: ')

        info = postMsg(msg)
        result = ""
        if info["code"] == "100000":
            print("send success")
            result = getMsg(msg)
        else:
            print("send failed")

        print("xiaobin: " + result)
