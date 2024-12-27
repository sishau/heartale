"""文字转语音"""
import asyncio
import sounddevice as sd
import soundfile as sf
import io
from tools import check_library_installed

class TTS:
    """获取待阅读文本的基础类
    """

    def __init__(self, key: str):
        """_summary_

        Args:
            key (str): 用于配置中区分使用本地什么服务
        """

        self.key = key
        self.conf = None

    def set_conf(self, conf, py_libs=None):
        """设置配置信息, 并可以初始化一些服务, 比如import第三方库, 防止未使用的TTS导致内存占用过大

        Args:
            conf (dict): 配置信息
            py_libs (list, optional): 依赖的第三方库. Defaults to None.

        Raises:
            ImportError: _description_
        """
        self.conf = conf
        if py_libs is not None:
            for py_lib in py_libs:
                if not check_library_installed(py_lib):
                    raise ImportError(f"请安装{py_lib}库: pip install {py_lib}")

    async def download(self, text):
        """下载
        """
        return text

    def play_audio(self, audio_data):
        audio, simple_rate = sf.read(io.BytesIO(audio_data), dtype='int16')
        device_index = sd.default.device[1]
        with sd.OutputStream(device=device_index, channels=1, samplerate=simple_rate, blocksize=1024):
            sd.play(audio, device=device_index, samplerate=simple_rate)
            sd.wait()

    async def play_mp3(self, audio_data, executor):
        """子线程朗读

        Args:
            audio_data (str): 音频数据
            executor (ThreadPoolExecutor): 线程池
        """

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(executor, self.play_audio, audio_data)
