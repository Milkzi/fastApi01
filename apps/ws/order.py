import time

# import requests
import httpx
import json
# from logger.http_log import logger
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
#
# # ssl._create_default_https_context = ssl._create_unverified_context
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from apps.redis_model import r
from apps.ws.util import filter_distance


class MyOrders:
    def __init__(self, token):

        self.now_time = int(time.time())
        self.headers = {
            "Accept": "application/json",
            "channel": "h5-tuiguangdashinew-ls",
            "os": "h5",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "Content-Type": "application/json,charset=utf-8",
            "Origin": "https://h5.huitouche.cn",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.27(0x18001b36) NetType/WIFI Language/zh_CN",
            "Referer": "https://h5.huitouche.cn/",
            "token": token
        }

        self.all_order_data = []
        self.query_local_order_header = {}
        self.query_local_order_res = {}
        self.one_match_order = {}
        # self.local_request = requests.session()
        # self.local_request.keep_alive = False
        self.one_match_order_id = ''
        self.success_order_id = ''
        self.lock_params = {}
        self.vehicle_id = ''
        self.mobile = ''
        self.driver_id = ''
        self.urls = {
            "wq_sign_url": "http://963e414695562663.natapp.cc:11112/sign",  # 加密
            "wq_decrypt_url": "http://963e414695562663.natapp.cc:11112/decrypt",  # 解密

            "local_url": "https://dispatch-api.huitouche.com/nearby/v2",  # 查询附近订单接口
            "back_url": "https://dispatch-api.huitouche.com/backhaul",

            "driver_url": "https://user-api.huitouche.com/profile/",
            "make_url": "https://order-api.huitouche.com/order/order_refresh/",

        }

    def get_wq_sign_header(self):
        data_json = {
            "index": "1",
            "radius_id": 510,
            "goods_types": "0",
            "app_cur_time": int(time.time() * 1000)
        }
        try:

            res = httpx.post(url=self.urls['wq_sign_url'], json=data_json,
                             timeout=1).json()
            self.query_local_order_header = res

            return True
        except Exception as e:
            print(e)
            return False

    # 查询附近的订单
    def query_local_order(self):
        json_data = self.query_local_order_header

        try:
            res = httpx.post(url=self.urls['local_url'], json=json_data,
                             headers=self.headers,
                             verify=False, timeout=3).json()
            print('查询附近的订单 返回结果--------\n' + json.dumps(res, ensure_ascii=False))
            if res["status"] == 100000:
                self.query_local_order_res = res
            return res
        except Exception as e:
            print(e)
        return False

    def get_decrypt_query_local_order_res(self):
        data_json = {"data": self.query_local_order_res.get("data", "")}
        try:
            res = httpx.post(url=self.urls['wq_decrypt_url'], json=data_json,
                             timeout=3).json()
            print(json.dumps(res, ensure_ascii=False))
            self.all_order_data = res['data']["list"]

            return True
        except Exception as e:
            print(e)
            return False

    #  锁定匹配的订单
    def lock_order(self, one_match_order, sponsor_type):
        lock_url = f"https://feed-api.huitouche.com/goods/{one_match_order['id']}/lock_refresh/"
        self.lock_params = {
            "price_expect": one_match_order['price']['price_expect'],
            "goods_id": one_match_order['id'],
            "price_addition": one_match_order['price']['price_addition'],
            "price_recommend": one_match_order['price']['price_recommend'],
            "is_phone_discuss": one_match_order['price']['is_phone_discuss'],
            "status": one_match_order['status'],
            "price_total": one_match_order['price']['price'],
            "price_type": one_match_order['price']['price_type'],
            "sponsor_type": sponsor_type,
            "is_agree_transport_protocol": 1,

        }

        try:
            res = httpx.post(url=lock_url, json=self.lock_params, headers=self.headers | {"appversion": "7.5.0"},
                             verify=False, timeout=3).json()
            print('匹配的订单返回结果-----\n' + json.dumps(res, ensure_ascii=False))

            return res

        except Exception as e:
            print(e)
        return False

    #  筛选订单
    @staticmethod
    async def filter_order(all_order_data, filter_message, websocket):
        start_time = time.perf_counter()
        filter_order_list = []
        # redis 过滤 司机洽谈中的订单
        print(f"filter_message----", filter_message)
        print(f"传入all_order_data----", all_order_data)
        print(f"传入all_order_data长度为----{len(all_order_data)}")
        print(r.smembers(filter_message["phone"]))

        if r.exists(filter_message["phone"]):
            all_order_data = list(
                filter(lambda x: str(x["id"]) not in r.smembers(filter_message["phone"]), all_order_data))
        print(f"过滤后的all_order_data长度为----{len(all_order_data)}")

        if filter_message.get("match_car_type"):  # 主动匹配车型
            for one_data in all_order_data:
                if any(list(filter(lambda x: x in one_data['vehicle_description'],
                                   filter_message.get("match_car_type").split("|")))):
                    filter_order_list.append(one_data)


                else:
                    await websocket.send(
                        json.dumps({
                            "msg": f"订单{one_data['id']}---车辆配置中未包含目标车型---{filter_message.get('match_car_type')}",
                            "level": 0},
                            ensure_ascii=False))

                    if not r.exists(filter_message["phone"]):
                        r.sadd(filter_message["phone"], one_data['id'])
                        r.expire(filter_message["phone"], 86400)
                    else:
                        r.sadd(filter_message["phone"], one_data['id'])
        else:
            filter_order_list = all_order_data

        print(f"match_car_type后长度为----{len(filter_order_list)}")

        if filter_message.get("screen_car_type"):
            for one_data in filter_order_list.copy():
                if any(list(filter(lambda x: x in one_data['vehicle_description'],
                                   filter_message.get("screen_car_type").split("|")))):
                    filter_order_list.remove(one_data)
                    await websocket.send(
                        json.dumps({
                            "msg": f"订单{one_data['id']}---车辆配置中包含有屏蔽车型---{filter_message.get('screen_car_type')}",
                            "level": 0},
                            ensure_ascii=False))
                    if not r.exists(filter_message["phone"]):
                        r.sadd(filter_message["phone"], one_data['id'])
                        r.expire(filter_message["phone"], 86400)
                    else:
                        r.sadd(filter_message["phone"], one_data['id'])

        print(f"screen_car_type后长度为----{len(filter_order_list)}")

        if filter_message.get("target_address"):
            for one_data in filter_order_list.copy():
                if any(list(filter(lambda x: x in one_data['to_location']['province']['name'
                ] + one_data['to_location']['city']['name'
                                             ] + one_data['to_location']['county']['name'
                                             ] + one_data['to_location']['town']['name'
                                             ] + one_data['to_location']['address'],
                                   filter_message.get("target_address").split("|")))):
                    pass
                else:
                    filter_order_list.remove(one_data)
                    await websocket.send(
                        json.dumps({
                            "msg": f"订单{one_data['id']}---目的地中未包含目标目的地---{filter_message.get('target_address')}",
                            "level": 0},
                            ensure_ascii=False))
                    if not r.exists(filter_message["phone"]):
                        r.sadd(filter_message["phone"], one_data['id'])
                        r.expire(filter_message["phone"], 86400)
                    else:
                        r.sadd(filter_message["phone"], one_data['id'])

        print(f"target_address后长度为----{len(filter_order_list)}")
        if filter_message.get("screen_address"):
            for one_data in filter_order_list.copy():
                if any(list(filter(lambda x: x in one_data['to_location']['province']['name'
                ] + one_data['to_location']['city']['name'
                                             ] + one_data['to_location']['county']['name'
                                             ] + one_data['to_location']['town']['name'
                                             ] + one_data['to_location']['address'],
                                   filter_message.get("screen_address").split("|")))):
                    filter_order_list.remove(one_data)
                    await websocket.send(
                        json.dumps({
                            # "msg": f"{one_data['to_location']['province']['name'] + one_data['to_location']['city']['name'] + one_data['to_location']['county']['name'] + one_data['to_location']['town']['name']}中包含有屏蔽目的地{filter_message.get('screen_address')}",
                            "msg": f"订单{one_data['id']}---目的地中包含有屏蔽目的地---{filter_message.get('screen_address')}",
                            "level": 0},
                            ensure_ascii=False))
                    if not r.exists(filter_message["phone"]):
                        r.sadd(filter_message["phone"], one_data['id'])
                        r.expire(filter_message["phone"], 86400)
                    else:
                        r.sadd(filter_message["phone"], one_data['id'])

        print(f"screen_address后长度为----{len(filter_order_list)}")

        if filter_message.get("min_price"):

            for one_data in filter_order_list.copy():
                print(one_data['price']['price'])
                if int(one_data['price']['price']) < int(filter_message.get("min_price")):

                    filter_order_list.remove(one_data)
                    await websocket.send(
                        json.dumps({
                            "msg": f"订单{one_data['id']}---价格:{one_data['price']['price']} < 传入最低价格:{filter_message.get('min_price')}",
                            "level": 0},
                            ensure_ascii=False))
                    if not r.exists(filter_message["phone"]):
                        r.sadd(filter_message["phone"], one_data['id'])
                        r.expire(filter_message["phone"], 86400)
                    else:
                        r.sadd(filter_message["phone"], one_data['id'])

        print(f"min_price后长度为----{len(filter_order_list)}")

        if filter_message.get("delivery_time"):

            for one_data in filter_order_list.copy():

                if any(list(filter(lambda x: x in one_data['time'],
                                   filter_message.get("delivery_time")))):
                    pass


                else:
                    filter_order_list.remove(one_data)
                    await websocket.send(
                        json.dumps({
                            "msg": f"订单{one_data['id']}---车辆送货时间不匹配---{one_data['time']}",
                            "level": 0},
                            ensure_ascii=False))

                    if not r.exists(filter_message["phone"]):
                        r.sadd(filter_message["phone"], one_data['id'])
                        r.expire(filter_message["phone"], 86400)
                    else:
                        r.sadd(filter_message["phone"], one_data['id'])

        print(f"delivery_time后长度为----{len(filter_order_list)}")

        if filter_message.get("max_distance"):
            for one_data in filter_order_list.copy():
                if filter_distance(one_match_order_data=one_data,
                                   min_distance=int(filter_message.get("min_distance")),
                                   max_distance=int(filter_message.get("max_distance"))):
                    pass
                else:
                    filter_order_list.remove(one_data)
                    await websocket.send(
                        json.dumps({
                            "msg": f"订单{one_data['id']}---车辆送货路程距离不匹配---",
                            "level": 0},
                            ensure_ascii=False))

                    if not r.exists(filter_message["phone"]):
                        r.sadd(filter_message["phone"], one_data['id'])
                        r.expire(filter_message["phone"], 86400)
                    else:
                        r.sadd(filter_message["phone"], one_data['id'])
        print(f"max_distance后的长度为----{len(filter_order_list)}")

        print("最后return----filter_order_list------", filter_order_list)

        print(time.perf_counter() - start_time)

        return filter_order_list
