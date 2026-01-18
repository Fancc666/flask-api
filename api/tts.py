import asyncio
import edge_tts
import hashlib
import os
import json
from flask import Blueprint, request

bp = Blueprint('tts', __name__, url_prefix='/api')

def responser(code, data):
    if type(data) != dict:
        data = {"msg": data}
    return json.dumps({
        "code": code,
        "data": data
    }, ensure_ascii=False)

class myTTS:
    def __init__(self, text):
        self.text = text
        self.voice = "zh-CN-XiaoxiaoNeural"
    def md5_name(self):
        md5_obj = hashlib.md5()
        md5_obj.update(self.text.encode("utf-8"))
        name = md5_obj.hexdigest()
        return name
    async def write_file(self, path):
        file_name = self.md5_name() + ".mp3"
        output_file = os.path.join(path, file_name)
        output_file = os.path.abspath(output_file)
        if os.path.exists(output_file):
            print("use cache", output_file)
            return output_file, file_name
        communicate = edge_tts.Communicate(self.text, self.voice)
        with open(output_file, "wb") as file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio" and "data" in chunk:
                    file.write(chunk["data"])
        return output_file, file_name

@bp.route('/tts')
def tts():
    text = request.args.get("text")
    stype = request.args.get("type") or "http"
    if text == None or text == "":
        return responser(1, "para 'text' is required")
    tts = myTTS(text)
    final_path = os.environ.get('TTS_PATH') if stype != "https" else os.environ.get('TTS_PATH_HTTPS')
    fpath, fname = asyncio.run(tts.write_file(final_path))
    # /www/wwwroot/dev.565455.xyz/tel/voice
    # print(fpath)
    return responser(0, {'filepath': fname})
