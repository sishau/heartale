'常量'
from servers.legado import LegadoServer
from servers.txt import TxtServer
from servers.reader import ReaderServer
from tts.coqui import CoquiTTS
from tts.edge import EdgeTTS
from tts.fish import FishTTS
from tts.g_tts import GTTS
from tts.ms_azure import AzureTTS
from tts.paddle_speech import PaddleSpeechTTS


def get_servers():
    """获取所有服务

    Returns:
        dict: 所有服务
    """

    return [
        LegadoServer(),
        TxtServer(),
        ReaderServer(),
    ]


def get_ttses():
    """获取所有服务

    Returns:
        dict: 所有服务
    """

    return [
        EdgeTTS(),
        AzureTTS(),
        GTTS(),
        CoquiTTS(),
        PaddleSpeechTTS(),
        FishTTS()
    ]
