#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import yaml
import importlib

project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(project_folder, 'config', 'config.yaml'), 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

def import_from_file(folder, module_name):
    spec = importlib.util.spec_from_file_location(module_name, os.path.join(project_folder, folder, module_name+".py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    class_obj = getattr(module, module_name)
    instance = class_obj(config[folder][module_name])
    return instance

server_name = config['server']['key']
SERVER = import_from_file('server', server_name)

# tts_name = config['tts']['key']
# TTS = import_from_file('tts', tts_name)
