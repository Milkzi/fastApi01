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
from .websocket_process import main


async def websocket_endpoint(ws: WebSocket, client_id: str):
    await ws.accept()
    try:
        while True:
            receive_data = await ws.receive_json()
            print(type(receive_data), receive_data)
            if receive_data["status"] == 10001:
                first_form = receive_data["formData"]

                input_headers = first_form["inputHeaders"]
                code = first_form["code"]
                from_id = {"from_province_id": first_form["form_province"],
                           "from_city_id": first_form["form_city"],
                           "from_county_id": first_form["form_area"]
                           }

                to_id = {"to_province_id": first_form["form_province2"],
                         "to_city_id": first_form["form_city2"],
                         "to_county_id": first_form["form_area2"]
                         }

                input_confirm = first_form["inputConfirm"]
                input_confirm_mobile = first_form["inputConfirm_mobile"]
                input_confirm_open = first_form["inputConfirmOpen"]

                input_car_config = first_form["inputCarConfig"]
                input_radius = int(first_form["inputRadius"])
                input_time = int(first_form["inputTime"])
                list_input_car_config = list(filter(None, input_car_config.split(" ")))
                required_args = {"input_headers": input_headers,
                                 "code": code,
                                 "from_id": from_id,
                                 "to_id": to_id,
                                 "input_confirm": input_confirm,
                                 "input_confirm_mobile": input_confirm_mobile,
                                 "input_confirm_open": input_confirm_open,
                                 "input_radius": input_radius,
                                 "input_time": input_time,
                                 "list_input_car_config": list_input_car_config,

                                 }
                print(ws)
                p = Process(target=main, args=(required_args,), name=client_id)
                p.start()
                print(p.pid)
            if receive_data["status"] == 10100:  # 确认
                pass
            if receive_data["status"] == 100200:  # 取消、关闭ws
                pass
    except WebSocketDisconnect:
        del ws
