#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

import os
import requests

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class edge:
    def __init__(self, conf):
        self.conf = conf
        self.url = f"http://{self.conf['ip']}:{self.conf['port']}/tts"
        

    def initialize(self):
        self.data = {"t": "", "v": self.conf.get("voice", "zh-CN-XiaoxiaoNeural"), "r": self.conf.get("rate", "0"), "p": self.conf.get("pitch", "0"), "o": self.conf.get("output", "audio-24khz-48kbitrate-mono-mp3")}

    def synthesize(self, text: str):
        self.data["t"] = text
        response = requests.post(self.url, json=self.data, timeout=10)
        if response.status_code == 200:
            return response.content
        else:
            return None

