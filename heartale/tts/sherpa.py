from tools import get_proxy_url
from tts import TTS
import aiohttp

class sherpa(TTS):
    """获取待阅读文本的基础类
    """

    def __init__(self):
        self.com = None
        self.proxy = None
        super().__init__("sherpa")

    def set_conf(self, conf):
        self.conf = conf
        self.url = f"http://{self.conf['ip']}:{self.conf['port']}/tts"
        self.data = {"sid": self.conf.get("sid", "0"), "speed": self.conf.get("speed", "1.0")}

    async def download(self, text):
        self.data["text"] = text
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=self.data, timeout=30) as response:
                mp3_file = await response.read()
        return mp3_file
