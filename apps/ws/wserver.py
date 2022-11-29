import asyncio
import json
import time
from util import stop_thread
import websockets
import threading
from qiang import test, task_start
from apps.redis_model import r

ws_set = set()
threading_list = []


def thread_func(websocket, filter_message):
    print("创建子线程----" + str(websocket.id) + "开启循环任务-----")

    async def async_inner():
        await task_start(websocket, filter_message)
        # while True:
        #     await websocket.send(str(time.time()))
        #     print(time.time())
        # await websocket.send(str(time.time()) + "-------" + str(websocket.id))
        #     await asyncio.sleep(2)

    asyncio.run(async_inner())
    print("线程-协程运行完毕,开始结束此线程")
    for i in threading_list:
        if str(i.name) == str(websocket.id):
            threading_list.remove(i)
            stop_thread(i)
            print(f"{i.name}--线程删除成功")




async def handler(websocket):
    print("新websocket_id----", websocket.id)
    while True:
        try:
            message = await websocket.recv()
            print(message)
            message = json.loads(message)
            print(message)
            if message["msg"] == "clear_screen_orders_id_list":
                if r.exists(message["phone"]):
                    r.delete(message["phone"])
            if websocket.id not in ws_set and message["msg"] == "first_info":
                first_message = message
                ws_set.add(websocket.id)
                t = threading.Thread(target=thread_func, args=(websocket, first_message), name=websocket.id)
                threading_list.append(t)
                t.start()
            print(f'当前线程个数--{len(threading_list)}个')
            print("交互完毕，阻塞接收中...")
        except Exception as e:
            print(e, "eeeee")
            print(f"进入异常,开始删除此线程,当前线程个数--{len(threading_list)}个")
            for i in threading_list:
                if str(i.name) == str(websocket.id):
                    threading_list.remove(i)
                    stop_thread(i)
                    print(f"{i.name}--线程删除成功")
            break
    await websocket.close()


async def main():
    async with websockets.serve(handler, "0.0.0.0", 8001,
                                ping_interval=0.5,
                                ping_timeout=3,
                                # max_queue=8,
                                # max_size=2**22,
                                # write_limit=2**18
                                ):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
