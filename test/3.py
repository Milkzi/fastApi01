#
# site= {{'name': '菜鸟教程', 'alexa': 10000, 'url': 'www.runoob.com'},
#        {'name': '菜鸟教程', 'alexa': 10000, 'url': 'www.runoob.com'},
#        {'name': '菜鸟教程', 'alexa': 10000, 'url': 'www.runoob.com'},
#        {'name': '菜鸟教程', 'alexa': 10000, 'url': 'www.runoob.com'}}
#
# site2= {{'name': '菜鸟教程', 'alexa': 10000},
#        {'name': '菜鸟教程', 'alexa': 10000, 'url': 'www.runoob.com'},
#        {'name': '菜鸟教程', 'alexa': 10000, 'url': 'www.runoob.com'},
#        {'name': '菜鸟教程', 'alexa': 10000, 'url': 'www.runoob.com'}}
#
#
# print(site2.difference(site))

# for i in []:
#        print("aaa")
#        print(i)
# element = site.pop('name')
# if 'name' in site:
#
#     site.pop('name')
# print(site)
import datetime
import threading
import time

# def filter_match_car_type(all_order_data, one_car_type):
#        if one_car_type in one_data['vehicle_description']:
#               filter_order_list.append(one_data)
thread_lock = threading.Lock()


def filter_screen_car_type(filter_order_list, filter_message):
    for one_data in filter_order_list:
        for one_car_type in filter_message.get("screen_car_type").split("|"):
            if one_car_type in one_data['vehicle_description']:
                thread_lock.acquire()
                filter_order_list.remove(one_data)
                thread_lock.release()


def filter_target_address(filter_order_list, filter_message):
    for one_data in filter_order_list:
        for one_address in filter_message.get("target_address").split("|"):
            if one_address not in one_data['to_location']['address']:
                thread_lock.acquire()
                filter_order_list.remove(one_data)
                thread_lock.release()


def filter_screen_address(filter_order_list, filter_message):
    for one_data in filter_order_list:
        for one_address in filter_message.get("screen_address").split("|"):
            if one_address in one_data['to_location']['address']:
                thread_lock.acquire()
                filter_order_list.remove(one_data)
                thread_lock.release()


def filter_order(all_order_data, filter_message):
    filter_order_list = []

    # if filter_message.get("match_car_type"):  # 主动匹配车型
    #     for one_data in all_order_data:
    #         for one_car_type in filter_message.get("match_car_type").split("|"):
    #             if one_car_type in one_data['vehicle_description']:
    #                 filter_order_list.append(one_data)
    #
    # if filter_message.get("screen_car_type"):
    #     threading.Thread(target=filter_screen_car_type, args=(filter_order_list, filter_message)).start()
    #
    # if filter_message.get("target_address"):
    #     threading.Thread(target=filter_target_address, args=(filter_order_list, filter_message)).start()
    #
    # if filter_message.get("screen_address"):
    #     threading.Thread(target=filter_screen_address, args=(filter_order_list, filter_message)).start()
    #
    # if filter_message.get("min_price"):
    #     for one_data in filter_order_list:
    #         if one_data['price']['price'] < int(filter_message.get("min_price")):
    #             filter_order_list.remove(one_data)
    for one_data in all_order_data:
        if all([any(filter(lambda x: x in one_data['vehicle_description'],
                           filter_message.get("match_car_type", "").split("|"))),
                not any(filter(lambda x: x in one_data['vehicle_description'],
                               filter_message.get("screen_car_type", "").split("|"))),
                any([any(filter(lambda x: x in one_data['to_location']['address'],
                                filter_message.get("target_address", "").split("|"))),
                     not filter_message.get("target_address", "")]),
                not any(filter(lambda x: x in one_data['to_location']['address'],
                               filter_message.get("screen_address", "").split("|"))),
                one_data['price']['price'] > int(filter_message.get("min_price", 0))]):
            filter_order_list.append(one_data)
    return filter_order_list


print("".split("|"))

print(any([any(filter(lambda x: x in "hucheng", ["h"])),not "h"]))
print(not any(filter(lambda x: x in "hucheng", [""])))

print(int(time.time() * 1000))
