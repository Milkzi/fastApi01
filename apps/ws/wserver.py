import asyncio
import time

import websockets
import threading

ws_set = set()
threading_list = []

import inspect

import ctypes


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""

    tid = ctypes.c_long(tid)

    if not inspect.isclass(exctype):
        exctype = type(exctype)

    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))

    if res == 0:

        raise ValueError("invalid thread id")

    elif res != 1:

        # """if it returns a number greater than one, you're in trouble,

        # and you should call it again with exc=NULL to revert the effect"""

        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)

        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def thread_func(websocket):
    async def async_inner():
        while True:
            # print(websocket_id)
            # print(time.time())
            print("当前线程的名称为:--", threading.current_thread().name,websocket.id)
            await websocket.send(str(time.time())+"-------"+str(websocket.id))
            await asyncio.sleep(2)
            # time.sleep(2)
    asyncio.run(async_inner())

async def handler(websocket):
    while True:
        try:
            message = await websocket.recv()
            print(websocket.id)
            print(message)
            print(type(message))
            await websocket.send(message)

            if websocket.id not in ws_set:
                ws_set.add(websocket.id)
                # websockett = copy.copy(websocket)
                t = threading.Thread(target=thread_func, args=(websocket,), name=websocket.id)
                threading_list.append(t)
                t.start()
            for i in threading_list:
                print("外部threading_list的name：", i.name)
                print("外部websocket.id：", websocket.id)
                print(type(i.name))
                print(i.name == websocket.id)
                if str(i.name) == str(websocket.id) and message == "close":
                    print("开始删除")
                    threading_list.remove(i)
                    stop_thread(i)

            print("交互完毕，阻塞接收中")
        except Exception as e:
            print(e,"eeeee")
            for i in threading_list:
                print("运行错误删除线程",i.name)
                if str(i.name) == str(websocket.id):

                    threading_list.remove(i)
                    stop_thread(i)
                    print("删除成功")
            break
    await websocket.close()


async def main():
    async with websockets.serve(handler, "localhost", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
