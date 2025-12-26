from flask import jsonify
import requests

def myResponse(code=0, msg='ok', data=None):
    return jsonify(
        code=code, 
        msg=msg, 
        data=[] if data is None else data
    )

def get_http(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/98.0.4758.82 Safari/537.36 "
    }
    html = requests.get(url, headers=headers)
    html.encoding = "utf-8"
    return html.text
