import os
PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://hucheng:hu697693@106.14.26.159/shengshengQ?charset=utf8mb4"

REDIS_URI = '106.14.26.159'


SS_Header = {
    "Accept": "application/json",
    "channel": "h5-tuiguangdashinew-ls",
    "os": "h5",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh-Hans;q=0.9",
    "Content-Type": "application/json,charset=utf-8",
    "Origin": "https://h5.huitouche.cn",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.27(0x18001b36) NetType/WIFI Language/zh_CN",
    "Referer": "https://h5.huitouche.cn/",
    "token": "7a2445b2-2941-41e6-b894-04bfe49049de"

}