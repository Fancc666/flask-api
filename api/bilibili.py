import requests
import json
from bilibili_api import homepage, search, sync
from flask import Blueprint, request

bp = Blueprint('bilibili', __name__, url_prefix='/api/bili')

class BiliDataGeter:
    def __init__(self) -> None:
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
        }
    def get_html(self, url):
        response = requests.get(url, headers=self.headers)
        response.encoding = "utf-8"
        return response.text
    def get_shouye(self):
        data = sync(homepage.get_videos())
        return data["item"]
    def get_search(self, keyword):
        data = sync(search.search(keyword))
        return data["result"][11]["data"]

def responser(code, data):
    if type(data) != dict:
        data = {"msg": data}
    return json.dumps({
        "code": code,
        "data": data
    }, ensure_ascii=False)

@bp.route("/shouye", methods=["GET"])
def bili_shouye():
    try:
        bili_case = BiliDataGeter()
        res = bili_case.get_shouye()
        return responser(0, res)
    except Exception as e:
        return responser(1, str(e))

@bp.route("/search", methods=["GET"])
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
