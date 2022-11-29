import json
import threading
import time
import asyncio
from typing import Optional, List
from fastapi import Cookie, Depends, FastAPI, Query, WebSocket, WebSocketDisconnect
from apps.utils.order import MyOrders
from multiprocessing import Process

from fastapi import Depends
from apps.utils.util import Aescrypt
from logger.http_log import logger
from apps.utils.order_executor import get_order_message, get_order_message_result
from starlette.websockets import WebSocketState
import random
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError


async def order_query(ws: WebSocket, required_args):
    vehicle_id = None  # 车辆配置ID
    driver_id = None  # 司机ID
    my_order = None  # 定义空订单
    try:
        my_order = MyOrders(headers=required_args['input_headers'], code=required_args["code"])
    except Exception as e:
        # del ws
        raise ConnectionClosedError

    while True:
        time.sleep(required_args['input_time'])

        print("开头", 1)
        # 1 查询附近订单或回头车订单
        if not required_args["input_confirm_open"]:
            # close_data = await ws.receive_json()
            # if close_data["status"] == 20404:
            #     print(20404001)
            #     raise WebSocketDisconnect(code=1000)
            await ws.send_json({"status": 10500, "msg": f"开始搜索附近订单..."})
            if not my_order.query_local_order(radius=required_args["input_radius"]): continue

        else:
            print("开头", 1111)
            # close_data = await ws.receive_json()
            # if close_data["status"] == 20404:
            #     print(20404002)
            #     raise WebSocketDisconnect(code=1000)
            await ws.send_json({"status": 10500, "msg": f"开始搜索附近订单..."})
            local_order_bool = my_order.query_local_order(radius=required_args["input_radius"])
            await ws.send_json({"status": 10500, "msg": f"开始搜索回头车订单..."})
            back_order_bool = my_order.query_back_order(from_id=required_args["from_id"], to_id=required_args["to_id"],
                                                        index=0)
            if not any([local_order_bool, back_order_bool]): continue

        await ws.send_json({"status": 10500, "msg": f"一共搜索到{len(my_order.all_order_data)}个订单"})
        match_order_list = []
        print(2)
        # 2 匹配车型配置订单
        for i in my_order.all_order_data:
            for j in required_args["list_input_car_config"]:
                if j in i['vehicle_description']:
                    match_order_list.append(i)
        # for i in my_order.all_order_data:
        #
        #     if i['price']['price'] == 2474:
        #         match_order_list.append(i)

        if len(match_order_list) == 0:
            await ws.send_json({"status": 10500, "msg": "车型适配失败,开始重新搜索新的订单..."})
            continue
        my_order.one_match_order = random.choice(match_order_list)
        my_order.one_match_order_id = my_order.one_match_order['id']

        print("当前的订单id是--", my_order.one_match_order_id)
        logger.info(json.dumps(my_order.one_match_order, ensure_ascii=False))
        await ws.send_json({"status": 10500, "msg": "车型适配成功..."})

        print(3)
        # 3 锁定匹配成功的订单
        # close_data = await ws.receive_json()
        # if close_data["status"] == 20404:
        #     print(20404002)
        #     raise WebSocketDisconnect(code=1000)
        lock_order_return = my_order.lock_order(have_phone_status=required_args["input_confirm_mobile"])
        if not lock_order_return: continue
        await ws.send_json({"status": 10500, "msg": "订单锁定成功..."})

        print(4)
        # 4 判断锁定订单状态
        if required_args["input_confirm"] and lock_order_return == 1:
            print("4.1给客户端发送锁定订单消息:")
            data_message = get_order_message(my_order=my_order)
            print(data_message)
            await ws.send_json({"status": 11000, "msg": "选择锁定订单是否抢单", "data": data_message})
            await ws.send_json({"status": 10500, "msg": "选择锁定订单是否抢单..."})
            num = 0
            is_confirm_message = {"status": 20200}
            while num < 30:
                time.sleep(1)
                print(num)
                is_confirm_message = await ws.receive_json()
                print(is_confirm_message["msg"])
                if is_confirm_message.get("status", 0) == 20100:
                    print(is_confirm_message)
                    break
                elif is_confirm_message.get("status", 0) == 20200:
                    print(is_confirm_message)
                    break
                elif is_confirm_message.get("status", 0) == 20404:
                    raise WebSocketDisconnect(code=1000)
                num += 1
            if is_confirm_message["status"] == 20100:
                vehicle_id = my_order.get_order_vehicle_id(vehicle_id=vehicle_id)
                driver_id = my_order.get_order_driver_id(driver_id=driver_id)
                my_order.make_order()
                if not my_order.query_order_result(): continue
                print("抢单状态成功")
                await ws.send_json({"status": 10500, "msg": "抢单成功..."})
                print("查单结果确认成功")
                # close_data = await ws.receive_json()
                # if close_data["status"] == 20404:
                #     print(20404002)
                #     raise WebSocketDisconnect(code=1000)
                data_message_result = get_order_message_result(my_order=my_order)
                print(data_message_result)
                await ws.send_json({"status": 12000, "msg": "返回抢单成功结果", "data": data_message_result})
                raise WebSocketDisconnect(code=1000)
            elif is_confirm_message["status"] == 20200:
                continue
        elif lock_order_return == 2 or not required_args["input_confirm"]:
            print("4.2给客户端发送锁定订单消息:")
            await ws.send_json({"status": 10500, "msg": "无需锁单，直接抢单..."})
            vehicle_id = my_order.get_order_vehicle_id(vehicle_id=vehicle_id)
            driver_id = my_order.get_order_driver_id(driver_id=driver_id)
            my_order.make_order()
            print("抢单状态成功")
            if not my_order.query_order_result(): continue
            await ws.send_json({"status": 10500, "msg": "抢单成功..."})
            # close_data = await ws.receive_json()
            # if close_data["status"] == 20404:
            #     print(20404002)
            #     raise WebSocketDisconnect(code=1000)
            data_message_result = get_order_message_result(my_order=my_order)
            print(data_message_result)
            await ws.send_json({"status": 12000, "msg": "返回抢单成功结果", "data": data_message_result})
            raise WebSocketDisconnect(code=1000)


def main(r):
    while True:
        time.sleep(1)