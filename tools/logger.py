#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from logging.config import dictConfig
import os
import yaml
from datetime import datetime

project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logger_folder = os.path.join(project_folder, 'logs')
if not os.path.exists(logger_folder):
    os.makedirs(logger_folder)
logger_file = "log_{}.log".format(datetime.now().strftime("%Y%m%d"))

# with open(os.path.join(project_folder, 'config', 'logger.yaml'), 'r', encoding='utf-8') as f:
#     logger_config = yaml.safe_load(f)

# logger_config['handlers']['file']['filename'] = os.path.join(logger_folder, logger_file)
# dictConfig(logger_config)
dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s]<%(filename)s:%(lineno)d>%(levelname)-8s: %(message)s',
            "datefmt": '%y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(asctime)s[%(module)s]%(levelname)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'filename': logger_file,
            'delay': True,
            'maxBytes': 5242880,
            'backupCount': 10,
            'encoding': 'utf8',
        }
    },
    'main': {
        'level': 'DEBUG',
        'handlers': ['console', 'file']
    }
})
logger = logging.getLogger("main")
logger.debug("Initializing logger module")