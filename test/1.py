from datetime import datetime

import websockets
import asyncio

from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError


async def webs(ws,path):
    try:
        while True:
            data = await ws.recv()
            print(data)

            await ws.send(str(datetime.now())+data)
    except ConnectionClosedOK as e:
        print("当前连接关闭")




if __name__ == '__main__':
    start_server = websockets.serve(webs,"localhost",8888)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()
    # task = asyncio.create_task(start_server)
    # asyncio.run()



