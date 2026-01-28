import configparser
from pathlib import Path
import os
import wordcloud
import jieba
import random
from flask import Blueprint, request
import json

bp = Blueprint('wordcloud', __name__, url_prefix='/api')

class Cloud:
    def __init__(self) -> None:
        val = os.environ.get("WC_PATH")
        assert val is not None
        self.IMGROOT = str(Path(val))

    def path(self, file_name):
        return str(Path(__file__).parent.parent / file_name)

    def get_config(self, key, type=str):
        configs = configparser.ConfigParser()
        configs.read(self.path("assets/wordcloudConfig.ini"))
        return type(configs["programme"][key])

    def getRandom(self):
        digits = "0123456789"
        ascii_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        str_list =[random.choice(digits+ascii_letters) for i in range(10)]
        random_str =''.join(str_list)
        return random_str

    def create_cloud(self, text):
        txt = text
        out = self.getRandom()+".png"
        txtlist = jieba.lcut(txt)
        words = " ".join(txtlist)
        stopwords = set()
        content = [line.strip() for line in open(self.path("assets/stop_words.txt"), 'r', encoding="utf-8").readlines()]
        stopwords.update(content)
        iw = self.get_config("image_width")
        ih = self.get_config("image_height")
        assert iw is not None and ih is not None
        w = wordcloud.WordCloud(background_color='white',
                                font_path=self.path("assets/" + self.get_config("font")), 
                                stopwords=stopwords, 
                                width=int(iw), 
                                height=int(ih),
                                mode="RGBA")
        w.generate(words)
        w.to_file(Path(self.IMGROOT) / out)
        return out

@bp.route('/wordcloud', methods=["POST"])
def wc():
    res = {
        "code": 0,
        "msg": "",
        "data": []
    }
    try:
        c = Cloud()
        p = c.create_cloud(request.get_json()["text"])
        res["msg"] = p
    except Exception as e:
        res["code"] = 1
        res["msg"] = str(e)
    res_text = "api_response=" + json.dumps(res, ensure_ascii=False)
    if request.args.get("type") == "json":
        return res_text
    return res
