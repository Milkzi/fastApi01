import time

import requests
from apps.utils.util import Aescrypt, random_device_id
import json
from logger.http_log import logger
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from model import db_session,FengData
# ssl._create_default_https_context = ssl._create_unverified_context
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class MyOrders:
    def __init__(self, headers,code):
        aescrypt = Aescrypt()
        self.headers = json.loads(aescrypt.decrypt_aes(headers))
        self.code = code
        self.now_time = int(time.time())
        logger.info(f"初始化当前时间{self.now_time}")
        self.headers = {k: v for k, v in self.headers.items() if k != "Host"}
        self.fang_feng_data = db_session.query(FengData).filter(FengData.code == self.code).all()
        assert self.fang_feng_data
        self.while_index = 0
        assert self.fang_feng_data[self.while_index].data.split(",")[:3][0]
        self.fang_feng_token = self.fang_feng_data[self.while_index].data.split(",")[:3][0]
        self.all_order_data = []
        self.one_match_order = {}
        self.one_match_order_id = ''
        self.success_order_id = ''
        self.lock_params = {}
        self.vehicle_id = ''
        self.mobile = ''
        self.driver_id = ''
        self.urls = {
            "local_url": "https://dispatch-api.huitouche.com/nearby",
            "back_url": "https://dispatch-api.huitouche.com/backhaul",


            "driver_url": "https://user-api.huitouche.com/profile/",
            "make_url": "https://order-api.huitouche.com/order/order_refresh/",

        }

    # 查询附近的订单
    def query_local_order(self, radius):
        time.sleep(2)
        self.all_order_data.clear()
        params = {
            "radius": radius,
            "index": 1
        }
        logger.info(f"当前时间{int(time.time())}")
        if int(time.time())-self.now_time > 60:
            print("切换token")
            self.while_index += 1
            if self.while_index > len(self.fang_feng_data):
                self.while_index = 0
            self.fang_feng_token = self.fang_feng_data[self.while_index].data.split(",")[:3][0]
            headers = self.headers | {"deviceId": random_device_id(),"token":self.fang_feng_token}
            self.now_time = int(time.time())
            logger.info(f"切换后当前token是{self.fang_feng_token}")
        else:
            logger.info(f"当前token是{self.fang_feng_token}")
            headers = self.headers | {"deviceId": random_device_id()}
        try:
            res = requests.get(url=self.urls.get('local_url'), params=params, headers=headers,
                               verify=False, timeout=3).json()
            logger.info('附近车查询api返回结果---------------\n'+json.dumps(res,ensure_ascii=False))
            if res["status"] == 100000:
                all_local_order_data = res["data"]['list']
                self.all_order_data.extend(all_local_order_data)
                if self.all_order_data:
                    return True
        except Exception as e:
            print(e)
        return False

    # 查询回头车 订单
    def query_back_order(self, from_id, to_id, index):
        time.sleep(2)
        headers = self.headers | {"deviceId": random_device_id(), "token": self.fang_feng_token}
        params = {
            "backhaul": 0,
            "from_city_id": from_id.get("from_city_id", 0),
            "from_county_id": from_id.get("from_county_id", 0),
            "from_province_id": from_id.get("from_province_id"),
            "from_town_id": 0,
            "goods_display_count": -1,
            "goods_types": '',
            "index": index,
            "loading_times": '',
            "manual_filter": 0,
            "only_booking": 0,
            "sort_type": 0,
            "to_city_id": to_id.get("to_city_id", 0),
            "to_county_id": to_id.get("to_county_id", 0),
            "to_province_id": to_id.get("to_province_id"),
            "to_town_id": 0,
            "vehicle_ids": '',
            "version": '',
        }
        try:
            res = requests.get(url=self.urls.get('back_url'), params=params, headers=headers,
                               verify=False, timeout=3).json()
            logger.info('回头车查询api返回结果------------\n' + json.dumps(res,ensure_ascii=False))
            if res["status"] == 100000:
                all_back_order_data = res["data"]["list"]
                self.all_order_data.extend(all_back_order_data)
                if self.all_order_data:
                    return True
        except Exception as e:
            print(e)
        return False

    #  锁定匹配的订单
    def lock_order(self, have_phone_status):
        time.sleep(2)
        lock_url = f"https://feed-api.huitouche.com/goods/{self.one_match_order_id}/lock_refresh/"
        self.lock_params = {
            "price_expect": self.one_match_order['price']['price_expect'],
            "goods_id": self.one_match_order['id'],
            "price_addition": self.one_match_order['price']['price_addition'],
            "price_recommend": self.one_match_order['price']['price_recommend'],
            "is_phone_discuss": self.one_match_order['price']['is_phone_discuss'],
            "status": self.one_match_order['status'],
            "price_total": self.one_match_order['price']['price'],
            "price_type": self.one_match_order['price']['price_type'],
        }


        try:
            res = requests.post(url=lock_url, json=self.lock_params, headers=self.headers,
                                verify=False, timeout=3).json()
            logger.info('锁定订单api返回结果-----\n' + json.dumps(res, ensure_ascii=False))
            if res['status'] == 100000:
                return 1
            elif res['status'] == 100404 and have_phone_status:
                return 2
        except Exception as e:
            print(e)
        return False

    #  获得订单所属  手机号码
    def get_order_phone(self):
        time.sleep(2)
        phone_url = f"https://user-api.huitouche.com/call/{self.one_match_order_id}"
        json_params = {
            "from_type": 1,
            "from_id": self.one_match_order_id
        }
        try:
            res = requests.post(url=phone_url, json=json_params, headers=self.headers,
                                verify=False, timeout=3).json()
            logger.info("获取订单结果手机号码信息返回-----\n" + json.dumps(res, ensure_ascii=False))
            if res["status"] == 100000:
                self.mobile = res['data']['mobile']
            elif res["status"] == 100006:
                self.mobile = 'token过期'
            else:
                self.mobile = '获取失败'
        except Exception as e:
            print(e)
            self.mobile = "获取异常"
        return True

    #  获得订单车辆信息  车辆ID
    def get_order_vehicle_id(self, vehicle_id):
        time.sleep(2)
        car_config_url = f"https://order-api.huitouche.com/order/vehicle_selection/?goods_id={self.one_match_order_id}"

        if vehicle_id:
            logger.info(f"缓存中获取车辆id成功-----{vehicle_id}")
            self.vehicle_id = vehicle_id
            return self.vehicle_id
        else:
            try:

                logger.info("订单车辆信息url-----------------\n" + car_config_url)
                res = requests.get(url=car_config_url, headers=self.headers,
                                   verify=False, timeout=3).json()
                logger.info("获得订单车辆信息返回-----\n"+json.dumps(res['data']['list'], ensure_ascii=False))
                vehicle_list = res['data']['list']
                if vehicle_list:
                    self.vehicle_id = vehicle_list[0]['id']
                    return self.vehicle_id
            except Exception as e:
                print(e)
        return False

    #  获得 司机ID
    def get_order_driver_id(self, driver_id):
        time.sleep(2)
        if driver_id:
            logger.info(f"缓存中获取司机id成功-----{driver_id}")
            self.driver_id = driver_id
            return self.driver_id
        else:
            try:
                res = requests.get(url=self.urls.get('driver_url'), headers=self.headers,
                                   verify=False, timeout=3).json()
                logger.info("获得司机ID信息返回-----\n" + json.dumps(res["data"]["user_id"], ensure_ascii=False))
                self.driver_id = res["data"]["user_id"]
                return self.driver_id
            except Exception as e:
                print(e)
        return False

    #  抢单
    def make_order(self):
        time.sleep(2)
        json_data = {
            "vehicle_id": self.vehicle_id,
            "driver_id": self.driver_id,
            "longitude": self.one_match_order['from_location']['longitude'],
            "latitude": self.one_match_order['from_location']['latitude'],
            "sponsor_type": 31,
            "goods_id": self.one_match_order['id'],
            "goods": self.lock_params,
            "price": self.lock_params['price_total'],
            "goods_owner_id": self.one_match_order['user_id'],
        }
        try:
            res = requests.post(url=self.urls.get('make_url'), json=json_data, headers=self.headers,
                                verify=False, timeout=3).json()
            logger.info("抢单信息返回-----\n" + json.dumps(res, ensure_ascii=False))
            if res["status"] == 100000:
                self.success_order_id = res["data"]["order_id"]
                return True
        except Exception as e:
            print(e)
        return True

    #  订单结果
    def query_order_result(self):
        time.sleep(2)
        result_url = f"https://order-api.huitouche.com/order/{self.success_order_id}"
        print(result_url)
        print(self.headers)
        try:
            res = requests.get(url=result_url, headers=self.headers,
                               verify=False, timeout=3).json()
            logger.info("查询订单结果信息返回-----\n" + json.dumps(res, ensure_ascii=False))
            if res["status"] == 100000:
                order_result_vehicle_id = res["data"]["driver"]["vehicle_id"]
                if order_result_vehicle_id == self.vehicle_id:
                    return True
        except Exception as e:
            print(e)
        return False
