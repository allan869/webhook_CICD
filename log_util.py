#!/usr/bin/env python
# coding:utf-8
import logging
from logging.handlers import TimedRotatingFileHandler
import os

if not os.path.exists('log'):
    os.mkdir('log')

fh = TimedRotatingFileHandler("log/logfile", when="midnight", encoding='utf-8')
# 创建一个logger
logger = logging.getLogger('mylogger')
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)

# 创建一个handler，用于写入日志文件
# fh = logging.FileHandler('test.log')
fh.setLevel(logging.DEBUG)
fh.setLevel(logging.INFO)

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setLevel(logging.INFO)

# 定义handler的输出格式
formatter = logging.Formatter('[%(asctime)s] [%(threadName)s] [%(module)s.%(funcName)s Line:%(lineno)d] [%(levelname)s]- %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)




def main():
    # 记录一条日志
    logger.info('foorbar')


if __name__ == '__main__':
    main()
