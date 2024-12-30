import os
import yaml
import importlib

project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(project_folder, 'config', 'config.yaml'), 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

def import_from_file(folder, module_name):
    spec = importlib.util.spec_from_file_location(module_name, os.path.join(project_folder, folder, module_name+".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    class_obj = getattr(module, module_name)
    instance = class_obj()
    return instance

server_name = config['server']['key']
SERVER = import_from_file('server', server_name)
server_config = config['server'][server_name]

tts_name = config['tts']['key']
TTS = import_from_file('tts', tts_name)
tts_config = config['tts'][tts_name]
