import datetime
import json
from apps.redis_model import r
from flask import Blueprint, jsonify, render_template, redirect, url_for, request, flash, g, session, Response, flash
from apps.flask.model.model import PhoneBindInfo
from apps.flask.model import db

api_app = Blueprint("api_app", import_name=__name__, url_prefix="/api")


@api_app.route("/query/phone/info", methods=['GET', "POST"], endpoint="query_phone_info")
def query_phone_info():
    if request.method == "GET":
        try:
            phone = request.args.get("phone")
            phone_info = PhoneBindInfo.query.filter(PhoneBindInfo.phone == phone).first()
            if phone_info:
                return jsonify({"status": 200, "msg": "查询成功", "data": {"phone": phone_info.phone,
                                                                       "token": phone_info.token,
                                                                       "match_car_type": phone_info.match_car_type,
                                                                       "screen_car_type": phone_info.screen_car_type,
                                                                       "target_address": phone_info.target_address,
                                                                       "screen_address": phone_info.screen_address,
                                                                       "min_price": phone_info.min_price,
                                                                       "min_distance": phone_info.min_distance,
                                                                       "max_distance": phone_info.max_distance,
                                                                       }})
            else:
                return jsonify({"status": 201, "msg": "数据为空", "data": {}})
        except Exception as e:
            print(e)
            return jsonify({"status": 400, "msg": "服务器异常", "data": {}})


@api_app.route("/add/phone/info", methods=['GET', "POST"], endpoint="add_phone_one_info")
def add_phone_one_info():
    if request.method == "POST":
        try:
            phone = request.args.get("phone")
            json_data = request.get_json()
            token = json_data.get("token")
            match_car_type = json_data.get("match_car_type")
            screen_car_type = json_data.get("screen_car_type")
            target_address = json_data.get("target_address")
            screen_address = json_data.get("screen_address")
            min_price = int(json_data.get("min_price"))
            min_distance = int(json_data.get("min_distance"))
            max_distance = int(json_data.get("max_distance"))
            phone_info = db.session.query(PhoneBindInfo).filter(PhoneBindInfo.phone == phone).scalar()
            if not phone_info:
                db.session.add(PhoneBindInfo(phone=phone,
                                             token=token,
                                             match_car_type=match_car_type,
                                             screen_car_type=screen_car_type,
                                             target_address=target_address,
                                             screen_address=screen_address,
                                             min_price=min_price,
                                             min_distance=min_distance,
                                             max_distance=max_distance,
                                             creat_time=datetime.datetime.now()))
                print("新增数据成功")

            else:
                phone_info.token = token
                phone_info.match_car_type = match_car_type
                phone_info.screen_car_type = screen_car_type
                phone_info.target_address = target_address
                phone_info.screen_address = screen_address
                phone_info.min_price = min_price
                phone_info.min_distance = min_distance
                phone_info.max_distance = max_distance
                phone_info.update_time = datetime.datetime.now()
                print("更新数据成功")
            db.session.commit()
            return jsonify({"status": 200, "msg": "添加成功", "data": phone})
        except Exception as e:
            print(e)
            return jsonify({"status": 400, "msg": "服务器异常", "data": ""})

@api_app.route("/clear/phone/screen/orders", methods=['GET', "POST"], endpoint="clear_phone_screen_orders")
def clear_phone_screen_orders():
    if request.method == "GET":
        try:
            phone = request.args.get("phone").strip()
            if phone:
                if r.exists(phone):
                    r.delete(phone)
                    return jsonify({"status": 200, "msg": f"{phone}的所有屏蔽订单,清除成功", "data": {}})
                else:
                    return jsonify({"status": 201, "msg": f"{phone}未有屏蔽订单信息", "data": {}})
            else:
                return jsonify({"status": 201, "msg": "网页中手机号为空", "data": {}})
        except Exception as e:
            print(e)
            return jsonify({"status": 400, "msg": "服务器异常", "data": {}})