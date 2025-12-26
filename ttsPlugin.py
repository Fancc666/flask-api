import asyncio
import edge_tts
import hashlib
import os

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
                if chunk["type"] == "audio":
                    file.write(chunk["data"])
        return output_file, file_name

if __name__ == '__main__':
    text = "你好"
    tts = myTTS(text)
    print(asyncio.run(tts.write_file('./data/')))
