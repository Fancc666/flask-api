# 改动前务必先检查，先pull再push
from flask import Flask, request, send_file
from flask import abort
from flask import jsonify
import json
import sys
import requests
import re
import time
import asyncio
import base64
from urllib import parse
from api import mailRequire
from api.biliRequire import BiliDataGeter
from api.ttsPlugin import myTTS

# sys.path.append("/Users/fcc/Desktop/Files/vs/pysqlite/bilidata-fans")
# sys.path.append("/root/FANCC/pys")
# sys.path.append("/Users/fcc/Desktop/Files/vs/pymail")
# sys.path.append("/root/FANCC/pymail")

# from db import *
# from api.cloudRequire import Cloud
# from maildb import MyMailDatabase
# from mailer import Mail
from api.lzRequire import lzDown
# def after_request(resp):
#     resp.headers['Access-Control-Allow-Origin'] = "*" # need to change!
#     resp.headers['Access-Control-Allow-Headers'] = "*"
#     return resp

# app.after_request(after_request)

app = Flask(__name__)

@app.after_request
def after_request(resp):
    origin = request.headers.get('Origin')
    if origin in {'https://www.565455.xyz', 'http://dev.565455.xyz', 'http://localhost:5500'}:
        resp.headers['Access-Control-Allow-Origin'] = origin
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return resp

def responser(code, data):
    if type(data) != dict:
        data = {"msg": data}
    return json.dumps({
        "code": code,
        "data": data
    }, ensure_ascii=False)

def empty(text):
    return text == None or text == ""

def get_http(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/98.0.4758.82 Safari/537.36 "
    }
    html = requests.get(url, headers=headers)
    html.encoding = "utf-8"
    return html.text

@app.route("/api")
def index():
    res = {
        "code": 0,
        "hello": "Hello Fancc API!"
    }
    res_text = "api_response=" + json.dumps(res)
    # res_text = jsonify(res)
    if request.args.get("type") == "json":
        return res_text
    return res

# @app.route("/api/wordcloud", methods=["POST"])
# def wc():
#     res = {
#         "code": 0,
#         "msg": "",
#         "data": []
#     }
#     try:
#         c = Cloud()
#         p = c.create_cloud(request.get_json()["text"])
#         res["msg"] = p
#     except Exception as e:
#         res["code"] = 1
#         res["msg"] = str(e)
#     res_text = "api_response=" + json.dumps(res, ensure_ascii=False)
#     if request.args.get("type") == "json":
#         return res_text
#     return res

@app.route("/api/mail", methods=["POST"])
def mail_api():
    res = {
        "code": 0,
        "msg": "",
        "data": []
    }
    try:
        # token
        tw = request.get_json()["to_whom"]
        sub = request.get_json()["subject"]
        ct = request.get_json()["content"]
        tk = tw + "+" + sub + "+" + ct
        tk_num = 0
        for x in tk:
            tk_num += ord(x)
        if base64.b64encode(str(tk_num).encode('utf-8')).decode('utf-8') != request.get_json()["token"]:
            res["code"] = 1
            res["msg"] = "token invalid"
        else:
            # send mail
            m = mailRequire.mail()
            m.message(tw, sub, ct)
            m.send()
    except Exception as e:
        res["code"] = 1
        res["msg"] = str(e)
    res_text = "api_response=" + json.dumps(res, ensure_ascii=False)
    if request.args.get("type") == "json":
        return res_text
    return res

@app.route("/api/send")
def send():
    try:
        link = str(request.args.get("l"))
        if link == "None" or link == "":
            return "para 'l' missing"
        h = get_http(link)
        return str(h)
    except Exception as e:
        return "ERR: " + str(e)
    
@app.route("/api/bili/shouye")
def bili_shouye():
    try:
        bili_case = BiliDataGeter()
        res = bili_case.get_shouye()
        return responser(0, res)
    except Exception as e:
        return responser(1, str(e))
    
@app.route("/api/bili/search")
def bili_search():
    param1 = request.args.get('s')
    if param1 != None:
        param1 = param1.strip()
    if param1 == None or param1 == "":
        return responser(1, "para 's' is required")
    try:
        bili_case = BiliDataGeter()
        res = bili_case.get_search(param1)
        return responser(0, res)
    except Exception as e:
        return responser(1, str(e))

@app.route("/api/tts")
def tts():
    text = request.args.get("text")
    rtype = request.args.get("type")
    if text == None or text == "":
        return responser(1, "para 'text' is required")
    tts = myTTS(text)
    fpath, fname = asyncio.run(tts.write_file("/www/wwwroot/dev.565455.xyz/tel/voice/"))
    # /www/wwwroot/dev.565455.xyz/tel/voice
    # print(fpath)
    if rtype == "media":
        return send_file(fpath, mimetype='audio/mpeg')
    return responser(0, {'filepath': fname})

@app.route("/api/lznew")
def lznew():
    lz = request.args.get("lz")
    if empty(lz):
        return responser(1, "para 'lz' is required")
    my_lz = lzDown()
    resp = my_lz.get_result(lz)
    # print(resp)
    return responser(0, resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
