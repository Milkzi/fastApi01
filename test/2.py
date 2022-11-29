import json
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


a = {"c": "1", "d": "2"}
fn(**a)

print(divmod(100, 1000)[1])
start_time = time.perf_counter()
header_lists = [header]
for i in header_lists:
    for j in ["zh", "ds", "sfsa"]:
        if j in i['Accept-Language']:
            header_lists.remove(i)
# time.sleep(1)
print(time.perf_counter() - start_time)
a = "{'is_vip_goods': 1, 'loading_time_period_begin': 1663578000, 'loading_time_period_end': 1663581600, 'id': 59638389, 'goods_weight': 0.5, 'is_rightnow': 0, 'vehicle_description': '小面包车', 'goods_create_time': '17:39下单', 'description': '', 'loading_time_is_realtime': 0, 'goods_level': 2, 'is_phone_discuss': 0, 'mileage': '', 'score': [], 'sort_score': {}, 'is_called': 0, 'vip_suggestion': {'params': {'prior_popup': '', 'prior_title': '', 'is_need_pop': 0, 'is_prior_contact': 0, 'prior_timer': 0, 'title': '', 'vip_type': 1, 'prior_left_seconds': 0, 'prior_app_end_time': 1663580427809}, 'type': 'web', 'page': ''}, 'haul_dist': 2, 'is_on_contact': 0, 'create_time': 1663580357, 'is_show_guide_price': 1, 'payment_method': 1, 'distance': 0, 'goods_type': 2, 'on_the_ways': ['广东省佛山市南海区大沥镇西湖路广佛五金城(广佛新城店)', '广东省阳江市阳西县织篢镇卡夫亨氏(阳江)食品有限公司(2号门)'], 'price_addition': 0, 'to_location': {'address': '中建科工集团有限公司致美斋阳西生产基地项目项目部', 'city': {'id': 441700, 'name': '阳江市'}, 'county': {'id': 441721, 'name': '阳西县'}, 'longitude': 111.584748, 'town': {'id': 441721100, 'name': '织篢镇'}, 'latitude': 21.765391, 'province': {'id': 440000, 'name': '广东省'}}, 'from_location': {'address': '鑫新电缆贸易有限公司', 'city': {'id': 440600, 'name': '佛山市'}, 'county': {'id': 440605, 'name': '南海区'}, 'longitude': 113.178314, 'town': {'id': 440605105, 'name': '大沥镇'}, 'latitude': 23.109945, 'province': {'id': 440000, 'name': '广东省'}}, 'is_system_price': 1, 'price': {'bonus': 0, 'price_type': 2, 'is_phone_discuss': 0, 'price_expect': 618, 'price': 618, 'is_prepaid': 0, 'need_driver_deposit': 0, 'peak_time_fee': 0, 'price_addition': 0, 'price_recommend': 618, 'price_without_peak_time_fee': 618}, 'status': 1, 'goods_name': '电缆线', 'is_booking': 0, 'user_id': 2652727, 'goods_volume': 2, 'extra_requires': [{'content': '不需要装卸', 'is_show_link': 0, 'extra_item_id': 1}, {'content': '0', 'is_show_link': 0, 'extra_item_id': 2}, {'content': '0', 'is_show_link': 0, 'extra_item_id': 3}, {'content': '0', 'is_show_link': 0, 'extra_item_id': 4}, {'content': '0', 'is_show_link': 0, 'extra_item_id': 5}], 'enabled_SXB': 0, 'total_called': 0, 'total_user_called': 0, 'carpool': 0, 'time': '今天 17:00-18:00', 'price_expect': 618}"
b = "{'is_vip_goods': 1, 'loading_time_period_begin': 1663580228, 'loading_time_period_end': 1663580828, 'id': 59638265, 'goods_weight': 0, 'is_rightnow': 1, 'vehicle_description': '小面包车', 'goods_create_time': '17:37下单', 'description': '', 'loading_time_is_realtime': 1, 'goods_level': 4, 'is_phone_discuss': 0, 'mileage': '', 'score': [], 'sort_score': {}, 'is_called': 0, 'vip_suggestion': {'params': {'prior_popup': '', 'prior_title': '', 'is_need_pop': 0, 'is_prior_contact': 0, 'prior_timer': 0, 'title': '会员优先', 'vip_type': 1, 'prior_left_seconds': 0, 'prior_app_end_time': 1663580429736}, 'type': 'web', 'page': ''}, 'haul_dist': 1, 'is_on_contact': 0, 'create_time': 1663580254, 'is_show_guide_price': 0, 'payment_method': 1, 'distance': 0, 'goods_type': 4, 'on_the_ways': ['广东省广州市海珠区南洲街道贝诺依服饰佳艺电脑绣花厂', '广东省广州市海珠区南洲街道华南致友创意园'], 'price_addition': 0, 'to_location': {'address': '华南致友创意园', 'city': {'id': 440100, 'name': '广州市'}, 'county': {'id': 440105, 'name': '海珠区'}, 'longitude': 113.341637, 'town': {'id': 440105016, 'name': '南洲街道'}, 'latitude': 23.053532, 'province': {'id': 440000, 'name': '广东省'}}, 'from_location': {'address': '湘源菜馆木桶饭连锁店(大塘店)', 'city': {'id': 440100, 'name': '广州市'}, 'county': {'id': 440105, 'name': '海珠区'}, 'longitude': 113.323478, 'town': {'id': 440105016, 'name': '南洲街道'}, 'latitude': 23.079694, 'province': {'id': 440000, 'name': '广东省'}}, 'is_system_price': 1, 'price': {'bonus': 0, 'price_type': 1, 'is_phone_discuss': 0, 'price_expect': 37, 'price': 37, 'is_prepaid': 1, 'need_driver_deposit': 0, 'peak_time_fee': 0, 'price_addition': 0, 'price_recommend': 37, 'price_without_peak_time_fee': 37}, 'status': 1, 'goods_name': '', 'is_booking': 0, 'user_id': 6852404, 'goods_volume': 0, 'extra_requires': [{'content': '不需要装卸', 'is_show_link': 0, 'extra_item_id': 1}, {'content': '0', 'is_show_link': 0, 'extra_item_id': 2}, {'content': '0', 'is_show_link': 0, 'extra_item_id': 3}, {'content': '0', 'is_show_link': 0, 'extra_item_id': 4}, {'content': '0', 'is_show_link': 0, 'extra_item_id': 5}], 'enabled_SXB': 0, 'total_called': 0, 'total_user_called': 0, 'carpool': 0, 'time': '现在用车 17:47', 'price_expect': 37}"

# print(json.loads(a))
# print(json.loads(b))
lock_order_res = {"status":0}
if lock_order_res['status'] == 100000:
    print("jin")
else:
    print("wu")