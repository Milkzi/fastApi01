

import requests
from flask import Blueprint, jsonify, request

import setting


ss_login_app = Blueprint("ss_login_app", import_name=__name__, url_prefix="/ss")


@ss_login_app.post("/send/code", endpoint="ss_login_send_code")
def ss_login_send_code():
    try:
        baseURL = 'https://account-api.huitouche.com/captcha/'
        submit_data = request.get_json()
        mobile = submit_data.get("mobile", "")

        post_data = {
            "mobile": mobile,
            "platform": 3,
            "type": 2
        }
        res = requests.post(url=baseURL, json=post_data, headers=setting.SS_Header).json()
        if res["status"] == 100000:
            return jsonify({"status": 10000, "msg":"发送成功"})
        else:
            return jsonify({"status": 10001, "msg": "发送失败"})
    except Exception as e:
        print(e)
        return jsonify({"status": 10404, "msg": "程序异常"})


@ss_login_app.post("/login", endpoint="ss_login_by_code")
def ss_login_by_code():
    """
    :param {"mobile":"","code":""}
    :return:
    """

    try:

        baseURL = 'https://account-api.huitouche.com/login/captch/'
        submit_data = request.get_json()
        mobile = submit_data.get("mobile", "")
        code = submit_data.get("code", "")

        post_data = {
            "mobile": mobile,
            "code": code,
            "user_type": 1
        }
        res = requests.post(url=baseURL, json=post_data, headers=setting.SS_Header).json()
        if res["status"] == 100000:
            return jsonify(
                {"status": 10000, "msg": "登录成功", "token": res["data"]["token"]})
        else:
            return jsonify({"status": 10001, "msg": "登录失败", "token": ""})
    except Exception as e:
        print(e)
        return jsonify({"status": 10404, "msg": "程序异常"})
