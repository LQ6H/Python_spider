# 单个视频下载
url = "https://v.douyin.com/JJ8kVTc/"  # 分享链接
session = requests.Session()
req = session.get(url, timeout=5, headers=HEADERS)
print(req.text)
video = re.findall(r'playAddr: "([\S]*?)"', req.text)[0]
vid = re.findall(r'vid=([\S]*?)&', video)[0]
addr = video.replace("/playwm/", "/play/")  # 去除水印
print(addr)
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
}
videoBin = session.get(addr, timeout=5, headers=headers)
with open('test.mp4', 'wb') as fb:
    fb.write(videoBin.content)


# 批量下载

import re
import requests
import os
header = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, sdch, br",
    "accept-language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
    "cache-control": "no-cache",
    "x-tt-logid": "202005280227480100140460221A4FD1CF",
    "x-tt-trace-host": "01ec7cfa064a667fc06b9359628310d7439e62ebd3f237434a2ab55522586ad295c69c0af06484df374b32e14ddb3f000f9912025769ad3b7c6273355e56a9332d1901cddf01df6db00b0b6f4b3f159082",
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    'cookie': 'tt_webid=6831576518742705677; _ba=BA0.2-20200528-5199e-qC83gMfiQQZIHGPAbWkc; _ga=GA1.2.1655972543.1590600365; _gid=GA1.2.843249182.1590600365'
}
data = {
    "sec_uid": "MS4wLjABAAAAlwXCzzm7SmBfdZAsqQ_wVVUbpTvUSX1WC_x8HAjMa3gLb88-MwKL7s4OqlYntX4r",
    "count": "21",
    "max_cursor": "0",
    "aid": "1128",
    "_signature": "1rexVRAciIE-bZMoZ46qv9a3sU",
    "dytk": "96ad80961288263ad9d1cff2895d0636"
}
url = "https://www.iesdouyin.com/web/api/v2/aweme/post"
url = "https://www.iesdouyin.com/share/user/4195355415549012?u_code=c23d6456gli&sec_uid=MS4wLjABAAAAlwXCzzm7SmBfdZAsqQ_wVVUbpTvUSX1WC_x8HAjMa3gLb88-MwKL7s4OqlYntX4r&timestamp=1590603009&utm_source=copy&utm_campaign=client_share&utm_medium=android&share_app_name=douyin"

response = requests.get(url, headers=header)


data = response.text
pattern = re.compile('"(https://aweme.snssdk.com/aweme/v1/play/.*?)"')
result = pattern.findall(data)
result = [i.split("&ratio")[0] for i in result]
result2 = [i.replace("/play/", "/playwm/") for i in result]

for i in result:
    print(i)
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
}
if not os.path.exists("无水印"):
    os.mkdir("无水印")
if not os.path.exists("水印"):
    os.mkdir("水印")

count = 0
for res1 in result:
    count += 1
    videoBin = requests.get(res1, timeout=5, headers=headers)
    with open(f'无水印/{count}.mp4', 'wb') as fb:
        fb.write(videoBin.content)
count = 0
for res2 in result2:
    count += 1
    videoBin = requests.get(res2, timeout=5, headers=headers)
    with open(f'水印/{count}.mp4', 'wb') as fb:
        fb.write(videoBin.content)
