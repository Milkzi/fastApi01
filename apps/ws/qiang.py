import asyncio
import datetime
import json
import random
import threading
import time

from order import MyOrders
from apps.redis_model import r

from concurrent.futures.thread import ThreadPoolExecutor


# from util import stop_thread
# from wserver import threading_list


async def test(websocket, filter_message):
    print("当前线程的名称为:--", threading.current_thread().name, websocket.id)


async def task_start(websocket, filter_message):
    my_order = MyOrders(filter_message['token'])
    first_while = True
    while True:
        if first_while:
            await websocket.send(json.dumps({"msg": "开始搜索...", "level": 0}, ensure_ascii=False))
            first_while = False
        else:
            new_time_interval = int(int(filter_message['time_interval']) / 100) * 100
            for i in range(new_time_interval, 0, -100):
                if divmod(i, 1000)[1] == 0:
                    await websocket.send(json.dumps({"msg": str(i), "level": 0}, ensure_ascii=False))
                time.sleep(0.1)
            else:
                if divmod(new_time_interval, 1000)[1] != 0:
                    await websocket.send(json.dumps({"msg": str(divmod(new_time_interval, 1000)[1]), "level": 0},
                                                    ensure_ascii=False))


        my_order.all_order_data = []
        get_header_result_status = my_order.get_wq_sign_header()
        if not get_header_result_status:
            await websocket.send(json.dumps({"msg": "获取加密请求头失败！", "level": 3}, ensure_ascii=False))
            continue
        query_local_order_result = my_order.query_local_order()
        if not query_local_order_result:
            print("省省搜索附近订单接口请求超时！")
            await websocket.send(json.dumps({"msg": "省省搜索附近订单接口请求超时！", "level": 3}, ensure_ascii=False))
            continue
        if query_local_order_result['status'] not in [100000, 100404]:
            msg = ""
            if query_local_order_result['msg']:
                msg = query_local_order_result['msg']
            elif query_local_order_result['message']:
                msg = query_local_order_result['message']
            await websocket.send(json.dumps({"msg": msg, "level": 3}, ensure_ascii=False))
            await websocket.send(json.dumps({"msg": "运行结束！！！", "level": 3}, ensure_ascii=False))
            break
        if not my_order.query_local_order_res:
            print("没有搜索到附近订单，重新搜索...")
            await websocket.send(json.dumps({"msg": "没有搜索到附近订单，重新搜索...", "level": 2}, ensure_ascii=False))
            continue
        decrypt_query_local_order_res_status = my_order.get_decrypt_query_local_order_res()
        if not decrypt_query_local_order_res_status:
            await websocket.send(json.dumps({"msg": "解密附近订单信息失败！", "level": 3}, ensure_ascii=False))
            continue

        if not my_order.all_order_data:
            print("没有搜索到附近订单，重新搜索...")
            await websocket.send(json.dumps({"msg": "没有搜索到附近订单，重新搜索...", "level": 2}, ensure_ascii=False))
            continue
        print("搜索到附近订单" + str(len(my_order.all_order_data)) + "个")
        await websocket.send(json.dumps({"msg": "成功搜索到附近订单" + str(len(my_order.all_order_data)) + "个", "level": 1},
                                        ensure_ascii=False))
        # 搜索附近订单成功,然后下一步

        filter_order_list = await my_order.filter_order(all_order_data=my_order.all_order_data,
                                                        filter_message=filter_message, websocket=websocket)
        if not filter_order_list:
            print("没有匹配到订单，重新搜索新的订单...")
            await websocket.send(json.dumps({"msg": "没有匹配到指定订单，重新搜索新的订单...", "level": 2}, ensure_ascii=False))
            continue
        print("成功匹配到附近" + str(len(filter_order_list)) + "个订单")
        await websocket.send(json.dumps({"msg": "成功匹配到附近" + str(len(filter_order_list)) + "个订单", "level": 1},
                                        ensure_ascii=False))  # 匹配成功，下一步等待2秒
        start_time = time.perf_counter()
        filter_order_list.sort(key=lambda x: x['price']['price'], reverse=True)
        lock_order_res = {"status": 0}
        print('开始锁单', time.perf_counter() - start_time)
        for index, one_match_order in enumerate(filter_order_list):
            await websocket.send(json.dumps({"msg": f"开始锁定第{index + 1}个匹配订单！", "level": 1}, ensure_ascii=False))
            sponsor_type = 23

            for i in range(2):
                # with ThreadPoolExecutor(max_workers=3) as execute:
                #     [execute.submit(my_order.lock_order).add_done_callback() for _ in range(3)]

                lock_order_res = my_order.lock_order(one_match_order=one_match_order, sponsor_type=sponsor_type)
                if not lock_order_res:
                    print(f"第{index + 1}个匹配订单----锁定接口超时！！！")
                    await websocket.send(
                        json.dumps({"msg": f"第{index + 1}个匹配订单----锁定接口超时！！！", "level": 3},
                                   ensure_ascii=False))
                    break
                if lock_order_res['status'] == 100000:
                    print(f"成功锁定第{index + 1}个匹配订单！！！")
                    print('锁单成功前', datetime.datetime.now())
                    await websocket.send(json.dumps({"msg": f"成功锁定第{index + 1}个匹配订单！", "level": 1}, ensure_ascii=False))
                    await websocket.send(
                        json.dumps({"msg": f"sshtc://home/goods/{one_match_order['id']}", "level": 1},
                                   ensure_ascii=False))

                    await websocket.send(
                        json.dumps({"msg": "锁单成功,停止运行！！！", "data": one_match_order,
                                    "level": 1}, ensure_ascii=False))
                    print('锁单成功后', datetime.datetime.now())
                    if not r.exists(filter_message["phone"]):
                        r.sadd(filter_message["phone"], one_match_order['id'])
                        r.expire(filter_message["phone"], 86400)
                    else:
                        r.sadd(filter_message["phone"], one_match_order['id'])

                    break
                if lock_order_res['status'] == 100404:
                    await websocket.send(
                        json.dumps({"msg": f"第{index + 1}个匹配订订单,第{i + 1}次尝试后返回100404", "level": 2}, ensure_ascii=False))
                    sponsor_type = 21
                else:
                    break

            if lock_order_res['status'] == 100000:
                break
            else:
                print('redis加锁失败前', time.perf_counter() - start_time)
                if not r.exists(filter_message["phone"]):
                    r.sadd(filter_message["phone"], one_match_order['id'])
                    r.expire(filter_message["phone"], 86400)
                else:
                    r.sadd(filter_message["phone"], one_match_order['id'])
                if lock_order_res['status'] != 100404:
                    print('锁单失败前', time.perf_counter() - start_time)
                    print(f"第{index + 1}个匹配订订单锁定失败！！！,f{lock_order_res['msg']}")
                    await websocket.send(
                        json.dumps({"msg": f"第{index + 1}个匹配订订单锁定失败！！！,{lock_order_res['msg']}",
                                    "level": 2},
                                   ensure_ascii=False))
                    print('锁单失败后', datetime.datetime.now())
        if lock_order_res['status'] == 100000:
            break
        else:
            print("--------------------全部锁定失败！重新搜索------------------")
            await websocket.send(
                json.dumps({"msg": "--------------------全部锁定失败！重新搜索------------------", "level": 2},
                           ensure_ascii=False))
            continue
