import configparser
import os
import wordcloud
import jieba
import random

class Cloud:
    def __init__(self) -> None:
        abs = os.path.abspath(__file__)
        self.ROOT = os.path.dirname(abs)
        self.IMGROOT = "/Users/fcc/Desktop/Files/vs/flask/data"
        # ///

    def path(self, file_name):
        return os.path.join(self.ROOT, file_name)

    def get_config(self, key, type=str):
        configs = configparser.ConfigParser()
        configs.read(self.path("config.ini"))
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
        content = [line.strip() for line in open(self.path("stop_words.txt"), 'r', encoding="utf-8").readlines()]
        stopwords.update(content)
        w = wordcloud.WordCloud(background_color='white',
                                font_path=self.path(self.get_config("font")), 
                                stopwords=stopwords, 
                                width=self.get_config("image_width", int), 
                                height=self.get_config("image_height", int),
                                mode="RGBA")
        w.generate(words)
        w.to_file(os.path.join(self.IMGROOT, out))
        return out

# def call(argv):
#     if len(argv) == 2:
#         return create_cloud(path(argv[0]), argv[1])
#     elif len(argv) == 1:
#         return create_cloud(path(argv[0]))

# if __name__ == "__main__":
#     argv = sys.argv
#     if len(argv) == 3:
#         create_cloud(path(argv[1]), argv[2])
#     else:
#         print("缺少参数")
