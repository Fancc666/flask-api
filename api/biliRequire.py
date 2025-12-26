import requests
import json
import re
from bilibili_api import homepage, search, sync

class BiliDataGeter:
    def __init__(self) -> None:
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
        }
    def get_html(self, url):
        response = requests.get(url, headers=self.headers)
        response.encoding = "utf-8"
        return response.text
    # def get_shouye(self):
    #     url = 'https://m.bilibili.com/'
    #     urlText = self.get_html(url)
    #     videoListText = re.findall(r'\"list\":(.*?),\"video\"', urlText)[0]
    #     videoList = json.loads(videoListText)
    #     return videoList["getHot-page-count-10-teenageMode-false-tinyMode-false"]["extra"]["list"]
    def get_shouye(self):
        data = sync(homepage.get_videos())
        return data["item"]
    def get_search(self, keyword):
        data = sync(search.search(keyword))
        return data["result"][11]["data"]
