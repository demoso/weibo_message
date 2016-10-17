# weibo_message
chat with microsoft xiaobing  based on python

## 微博模拟登录

1.通过fiddler抓包，找到登录请求地址，并分析相关参数
```Python
https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)
```
2.相关参数如下：
```Python
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
```
3.用户名base64编码
```Python
username = base64.b64encode(username.encode('utf-8')).decode('utf-8')
```
4.requests请求
```Python
session = requests.Session()
res = session.post(url, data = params)
```
5.汇总
```Python
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
```
## 与微软小冰私信
1.打开浏览器，登录微博，切换到私信页面，（以chrome浏览器为例）
2.fiddler抓包，查看并分析cookie
3.实时获取Chrome浏览器cookie,防止超时
```Python
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
```
4.给微软小冰发送私信，带上相关cookie,请求采用PC端发送私信请求url, 移动端实测发送不成功，不能成功入库
```Python
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

```
5.获取小冰最新回答，采用移动端请求信息url,移动端发挥json格式，比较容易解析
```Python
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
```
## 源码地址
源码传送门： [https://github.com/zuojj/weibo_message](https://github.com/zuojj/weibo_message)

## 参考地址
* [Python3从chrome浏览器读取cookie](http://www.jianshu.com/p/cd2117b931e3)
* [Python 模拟登录新浪微博的两种方法](http://lovenight.github.io/2015/11/23/Python-%E6%A8%A1%E6%8B%9F%E7%99%BB%E5%BD%95%E6%96%B0%E6%B5%AA%E5%BE%AE%E5%8D%9A/)
