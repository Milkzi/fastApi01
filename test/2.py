import time

# from apps.utils.util import random_device_id

header = {
  "deviceId": "c1c49bbb7ba6433c763",
  "channel": "ios",
  "os": "ios 15.4.1",
  "Accept-Encoding": "br;q\u003d1.0, gzip;q\u003d0.9, deflate;q\u003d0.8",
  "appVersion": "6.10.1",
  "operationSystem": "ios",
  "User-Agent": "SSHuitouche/6.10.1 (com.huitouche.HTC; build:6.10.1.2; iOS 15.4.1) Alamofire/5.4.4UIDevice",
  "Accept-Language": "zh-Hans-CN;q\u003d1.0",
  "token": "8902ea97-3433-4a25-be51-85c626ebf6fa",
  "apiVersion": "4.0"
}
# headers = header | {"deviceId": random_device_id()}

print(header)
# print(headers)
print(time.perf_counter())
def fn(**f):
  print(f)
  for i in f.items():
    print(i)

a = {"c":"1","d":"2"}
fn(**a)


