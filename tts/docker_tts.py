from tools import get_proxy_url
from tts import TTS
import aiohttp

class dockerTTS(TTS):
    """获取待阅读文本的基础类
    """

    def __init__(self):
        self.com = None
        self.proxy = None
        super().__init__("edge")

    def set_conf(self, conf):
        self.conf = conf
        self.url = f"http://{self.conf['ip']}:{self.conf['port']}/tts"
        self.data = {"t": "", "v": self.conf.get("voice", "zh-CN-XiaoxiaoNeural"), "r": self.conf.get("rate", "0"), "p": self.conf.get("pitch", "0"), "o": self.conf.get("output", "audio-24khz-48kbitrate-mono-mp3")}

    async def download(self, text, file):
        self.data["t"] = text
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=self.data, timeout=10) as response:
                mp3_file = await response.read()
        with open(file, "wb") as f:
            f.write(mp3_file)
        return True
