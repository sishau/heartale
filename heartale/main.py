"""主文件"""
import asyncio
import os
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from servers import Server
from tools.config import (get_config, get_config_server,
                    get_config_tts_download, get_config_max_time)
from tools.constant import get_servers, get_ttses
from tools.count import save_read_time
from tts import TTS


def get_server(conf_all) -> Server:
    """基础类的扩展

    Args:
        conf_all (dict): 完整配置

    Returns:
        Server: _description_
    """
    key, conf_server = get_config_server(conf_all)

    for s in get_servers():
        if s.key == key:
            s.set_conf(conf_server)
            return s

    print(f"未知的服务 {key}")
    return None


def get_tts(conf_all) -> TTS:
    """获取tts服务

    Args:
        conf_all (dict): _description_

    Returns:
        TTS: _description_
    """

    key, conf_tts = get_config_tts_download(conf_all)

    for tts in get_ttses():
        if tts.key == key:
            tts.set_conf(conf_tts)
            return tts

    print(f"未知的服务 {key}")
    return None


def print_test(i, chap, text):
    """_summary_

    Args:
        i (_type_): _description_
        chap (_type_): _description_
        text (_type_): _description_
        file (_type_): _description_
    """
    print(f"*** {i}/{chap} ***")
    if len(text) > 20:
        print(f"{text[:20]} ... {len(text)}")
    else:
        print(text[:20])


async def play():
    """主函数
    """
    # https://github.com/gedoor/legado
    # 获取当前第一本书的信息
    st = time.time()

    # 本次阅读开始时间
    date_key = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"开始时间：{date_key}")
    # 每次阅读多久
    read_time_data = {
        "word": [],
        "time": []
    }

    conf = get_config()
    proxy_url = conf.get("proxy_url", "")
    chap, play_min = get_config_max_time(conf)

    if len(proxy_url) > 0:
        print(proxy_url)
        # 设置环境变量
        os.environ['http_proxy'] = proxy_url
        os.environ['https_proxy'] = proxy_url

    tts = get_tts(conf)
    server = get_server(conf)

    print(f"初始化完成:tts:{tts.key}, txt:{server.key}")
    print("下载中，请稍等……")

    executor = ThreadPoolExecutor(max_workers=1)

    # 下载和播放章节
    text = await server.initialize()
    task_download = asyncio.create_task(tts.download(text))
    # 默认听100章节，自动停止
    for _i in range(chap):
        # 默认播放100分钟，一段结束再停止
        if sum(read_time_data["time"]) > play_min * 60:
            print(f'阅读{(sum(read_time_data["time"]))/60} > {play_min}分钟')
            break

        read_time_data["time"].append(round(time.time() - st, 2))
        read_time_data["word"].append(len(text))
        save_read_time(date_key, read_time_data, server.book_name)
        st = time.time()

        # 并行播放和下载任务
        audio_data = await task_download
        task_play = asyncio.create_task(tts.play_mp3(audio_data, executor))

        text = await server.next()
        print_test(_i, chap, text)

        task_download = asyncio.create_task(tts.download(text))

        await task_play

if __name__ == '__main__':
    """运行主函数"""
    asyncio.run(play())
