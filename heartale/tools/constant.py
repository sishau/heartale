'常量'
from servers.legado import LegadoServer
from servers.txt import TxtServer
from servers.reader import ReaderServer
from tts.docker_tts import dockerTTS
from tts.sherpa import sherpa

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
        dockerTTS(),
        sherpa()
    ]
