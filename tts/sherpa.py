#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

import os
import yaml
import sherpa_onnx
import soundfile as sf
import io
from tools import logger

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class sherpa:
    def __init__(self, conf):
        self.conf = conf
        self.tts_server = None

    def initialize(self):
        model_config = yaml.safe_load(open(os.path.join(project_dir, self.conf['model_config']), "r"))
        # model_dir = os.path.join(project_dir, model_config['model_folder'])
        model_dir = model_config.get("model_folder", "./models")
        if "rule_fsts" in model_config:
            rule_fsts = [os.path.join(model_dir, rule_fst.strip()) for rule_fst in model_config["rule_fsts"].split(",")]
            rule_fsts = ",".join(rule_fsts)
        else:
            rule_fsts = ""
        model_config = {key:os.path.join(model_dir, value) for key, value in model_config.items() if key not in ("model_folder", "rule_fsts")}

        tts_config = sherpa_onnx.OfflineTtsConfig(
            model=sherpa_onnx.OfflineTtsModelConfig(
                vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                    model=model_config.get("model", "./models/model.onnx"),
                    lexicon=model_config.get("lexicon", ""),
                    data_dir=model_config.get("data_dir", ""),
                    dict_dir=model_config.get("dict_dir", ""),
                    tokens=model_config.get("tokens", "./models/tokens.txt")
                ),
                matcha=sherpa_onnx.OfflineTtsMatchaModelConfig(),
                provider="cpu",
                debug=False,
                num_threads=1,
            ),
            rule_fsts=rule_fsts,
            max_num_sentences=1,
        )
        if not tts_config.validate():
            raise ValueError("Please check your config")
        self.tts_server = sherpa_onnx.OfflineTts(tts_config)

    def synthesize(self, text: str):
        sid = self.conf.get("sid", 0)
        speed = self.conf.get("speed", 1.0)
        audio = self.tts_server.generate(text, sid=sid, speed=speed)
        if audio is None:
            return None
        buffer = io.BytesIO()
        sf.write(buffer, audio.samples, samplerate=audio.sample_rate, format="WAV")
        buffer.seek(0)
        return buffer


