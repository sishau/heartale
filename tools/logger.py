import logging
import os
import yaml
from datetime import datetime
from tools.constant import *

logger_folder = os.path.join(project_folder, 'logs')
if not os.path.exists(logger_folder):
    os.makedirs(logger_folder)
logger_file = "log_{}.log".format(datetime.now().strftime("%Y-%m-%d"))

with open(os.path.join(project_folder, 'config', 'logger.yaml'), 'r', encoding='utf-8') as f:
    logger_config = yaml.safe_load(f)

logger_config['handlers']['file']['filename'] = os.path.join(logger_folder, logger_file)

logging.config.dictConfig(logger_config)

logger = logging.getLogger('main')

