import logging
import os
from datetime import datetime

from ..config import LOG_DIR

# 创建一个日志目录，如果不存在的话
log_dir = 'logs'

# 配置日志文件名
log_filename = os.path.join(LOG_DIR, 'message', f'{datetime.now().strftime("%Y-%m-%d")}.log')

# 创建一个独立的logger，避免与现有logger冲突
message_logger = logging.getLogger('MessageLogger')

# 设置日志级别，确保能捕获DEBUG级别的日志
message_logger.setLevel(logging.DEBUG)

# 配置日志格式
log_format = '%(asctime)s [MSG] | %(message)s'
formatter = logging.Formatter(log_format, datefmt='%H:%M:%S')

# 创建一个FileHandler，将日志写入指定的文件
file_handler = logging.FileHandler(log_filename)
file_handler.setFormatter(formatter)

# 添加FileHandler到MessageLogger
message_logger.addHandler(file_handler)

