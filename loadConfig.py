#!/usr/bin/env python

__author__ = "Gaurav Pundir"


import colorlog
import logging
import os
import ruamel.yaml

with open("config.yaml","r") as fp:
    config = ruamel.yaml.round_trip_load(fp)

def create_logger(debug=False):
    """
        Setup the logging environment
    """
    log = logging.getLogger()  # root logger
    logLevel = logging.DEBUG if debug else logging.INFO
    log.setLevel(logLevel)
    format_str = '%(asctime)s - %(levelname)-8s - %(filename)s - Line : %(lineno)d - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    if  os.isatty(2):
        cformat = '%(log_color)s' + format_str
        colors = {'DEBUG': 'reset',
                  'INFO': 'reset',
                  'WARNING': 'bold_yellow',
                  'ERROR': 'bold_red',
                  'CRITICAL': 'bold_red'}
        formatter = colorlog.ColoredFormatter(cformat, date_format,
                                              log_colors=colors)
    else:
        formatter = logging.Formatter(format_str, date_format)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)
    return logging.getLogger(__name__) 
