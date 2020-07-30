# -*- coding:utf-8 -*-
import logging, os
from logging.handlers import RotatingFileHandler


class Logger:
    
    def __init__(self, loggername, logfilepath):
        
        #创建一个logger
        self.logger  = logging.getLogger(loggername)
        self.logger.setLevel(logging.DEBUG)

        #创建一个handler，用于写入日志文件
        log_path = os.path.dirname(logfilepath + "/logs/")
        logname =  log_path + 'out.log'
        fh = RotatingFileHandler(logname, maxBytes=1024*1024*100, backupCount=1)
        fh.setLevel(logging.DEBUG)

        #创建一个handler，用于将日志输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)