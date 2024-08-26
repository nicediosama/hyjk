#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import time
import hashlib
import requests
from oceanengine.report_material_get import report_material_get
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, jsonify, render_template
from flybook import *
import time
from flybook import *

# const
# 随机字符串，用于签名生成加密使用
NONCE_STR = "13oEviLbrTo458A3NjrOwS70oTOXVOAm"

# 从 .env 文件加载环境变量参数
load_dotenv(find_dotenv())

# 初始化 flask 网页应用
app = Flask(__name__, static_url_path="/public", static_folder="./public")

# 获取环境变量
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
FEISHU_HOST = os.getenv("FEISHU_HOST")

# 应用出现错误时，使用flask的errorhandler装饰器实现应用错误处理
@app.errorhandler(Exception)
def auth_error_handler(ex):
    response = jsonify(message=str(ex))
    response.status_code = (
        ex.response.status_code if isinstance(ex, requests.HTTPError) else 500
    )
    return response


# 用获取的环境变量初始化Auth类，由APP ID和APP SECRET获取access token，进而获取jsapi_ticket
GAT = Get_Access_Token()

# 默认的主页路径
@app.route("/", methods=["GET"])
def get_home():
    # 打开本网页应用执行的第一个函数
    # 展示主页
    return render_template("index.html")

# 获取并返回接入方前端将要调用的config接口所需的参数
@app.route("/get_config_parameters", methods=["GET"])
def get_config_parameters():    
    # 接入方前端传来的需要鉴权的网页url
    url = request.args.get("url")
    # 初始化Auth类时获取的jsapi_ticket
    ticket = GAT.get_jsapi_ticket()
    # 当前时间戳，毫秒级
    timestamp = int(time.time()) * 1000
    # 拼接成字符串 
    verify_str = "jsapi_ticket={}&noncestr={}&timestamp={}&url={}".format(
        ticket, NONCE_STR, timestamp, url
    )
    # 对字符串做sha1加密，得到签名signature
    signature = hashlib.sha1(verify_str.encode("utf-8")).hexdigest()
    # 将鉴权所需参数返回给前端
    return jsonify(
        {
            "appid": APP_ID,
            "signature": signature,
            "noncestr": NONCE_STR,
            "timestamp": timestamp,
        }
    )

@app.route('/backend', methods=['GET'])
def backend():
    text = request.args.get("text")
    print(text)
    # 获取千川数据
    data_dict = report_material_get()
    # 多维表格地址
    table = Table('https://pvca9kku524.feishu.cn/base/DIixbNfRGapT6nsG7p5czpB4nUe?table=tblLxmV6mRr8yz30&view=vewJI9vdRo')
    
    R = Record()
    for item in data_dict["data"]["list"]:
        material_id = item["material_id"]
        print(type(material_id))
        fields = {
            "文本": str(material_id),
            "日期": int(time.time() * 1000)
        }
        R.create_a_record(fields, table.parent_node, table.table_id)
        print(material_id)

    # 返回处理后的文本给前端
    return jsonify(
        {
            'processed_text': data_dict
        }
    )

if __name__ == "__main__":
    # 以debug模式运行本网页应用
    # debug模式能检测服务端模块的代码变化，如果有修改会自动重启服务
    app.run(host="0.0.0.0", port=3000, debug=True)
