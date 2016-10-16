#coding=utf8

# 2016-10-10
# @author Benjamin(zuojj.com@gmail.com)
# @home http://www.zuojj.com

import time
import json
import base64
import os
import sqlite3
import requests
from win32.win32crypt import CryptUnprotectData

# @method getPrivateMsgCookie
# @description 获取私信发送请求头cookie, 本例获取windows7 chrome browser cookie
# @param host 当前host
# @return cookie

def getPrivateMsgCookie(host = '.weibo.com'):
    # windows7 Chrome cookies file path
    cookiepath = os.environ['LOCALAPPDATA'] + r"\Google\Chrome\User Data\Default\Cookies"

    sql = "select host_key,name,encrypted_value from cookies where host_key='%s'" % host
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


# @method postMsg
# @description 给微软小冰发送私信
# @param msg 私信内容
# @return info 响应info
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

# @method getMsg
# @description 递归获取小冰回答信息，由于获取延迟，采用递归方式
# @msg 发送给小冰信息
# @return 返回小冰回答信息

get_url = "http://m.weibo.cn/msg/messages?uid=5175429989&page=1"
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

def getMsg(msg):
    response = requests.get(get_url, headers=get_headers)
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

