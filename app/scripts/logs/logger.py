import os
import logging
from logging.handlers import RotatingFileHandler

import colorlog

from ..config import bot_settings, LOG_DIR

# 日志格式
# 09-10 20:25:98 [INFO] name | message
class Log_Colors:
    RESET = "\033[0m"
    RED = "\033[31m"    # 错误
    GREEN = "\033[32m"  # 信息
    YELLOW = "\033[33m" # 警告
    BLUE = "\033[34m"   # 调试

log_colors_config = {
    # 终端输出日志颜色配置
    'DEBUG': 'cyan',
    'INFO': 'white',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

default_formats = {
    # 终端输出格式
    'color_format': '\033[32m%(asctime)s\033[0m [%(log_color)s%(levelname)s\033[0m]\033[0m \033[34m%(name)s\033[0m | %(message)s',
    # 日志输出格式
    'log_format': '%(asctime)s [%(levelname)s] %(name)s | %(message)s'
}

if bot_settings.LOG_LEVEL == 'debug':
    set_log_level = logging.DEBUG
else:
    set_log_level = logging.INFO


class HandleLog:
    """
    先创建日志记录器（logging.getLogger），然后再设置日志级别（logger.setLevel），
    接着再创建日志文件，也就是日志保存的地方（logging.FileHandler），然后再设置日志格式（logging.Formatter），
    最后再将日志处理程序记录到记录器（addHandler）
    """

    def __init__(self):
        self.__all_log_path = os.path.join(LOG_DIR, f"log.log")  # 收集所有日志信息文件
        self.__error_log_path = os.path.join(LOG_DIR, f"log-error.log")  # 收集错误日志信息文件
        self.__logger = logging.getLogger('kokomibot')  # 创建日志记录器
        self.__logger.setLevel(set_log_level)  # 设置日志记录器记录级别

    @staticmethod
    def __init_logger_handler(log_path):
        """
        创建日志记录器handler，用于收集日志
        """
        logger_handler = RotatingFileHandler(filename=log_path, maxBytes=10 * 1024 * 1024, backupCount=2, encoding='utf-8')
        return logger_handler

    @staticmethod
    def __init_console_handle():
        """创建终端日志记录器handler，用于输出到控制台"""
        console_handle = colorlog.StreamHandler()
        return console_handle

    def __set_log_handler(self, logger_handler, level=logging.DEBUG):
        """
        设置handler级别并添加到logger收集器
        """
        logger_handler.setLevel(level=level)
        self.__logger.addHandler(logger_handler)

    def __set_color_handle(self, console_handle):
        """
        设置handler级别并添加到终端logger收集器
        """
        console_handle.setLevel(logging.DEBUG)
        self.__logger.addHandler(console_handle)

    @staticmethod
    def __set_color_formatter(console_handle, color_config):
        """
        设置输出格式-控制台
        """
        formatter = colorlog.ColoredFormatter(default_formats["color_format"], datefmt='%m-%d %H:%M:%S', log_colors=color_config)
        console_handle.setFormatter(formatter)

    @staticmethod
    def __set_log_formatter(file_handler):
        """
        设置日志输出格式-日志文件
        """
        formatter = logging.Formatter(default_formats["log_format"], datefmt='%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)

    @staticmethod
    def __close_handler(file_handler):
        """
        关闭handler
        """
        file_handler.close()

    def __console(self, level, message):
        """
        构造日志收集器
        """
        all_logger_handler = self.__init_logger_handler(self.__all_log_path)  # 创建日志文件
        error_logger_handler = self.__init_logger_handler(self.__error_log_path)
        console_handle = self.__init_console_handle()

        self.__set_log_formatter(all_logger_handler)  # 设置日志格式
        self.__set_log_formatter(error_logger_handler)
        self.__set_color_formatter(console_handle, log_colors_config)

        self.__set_log_handler(all_logger_handler)  # 设置handler级别并添加到logger收集器
        self.__set_log_handler(error_logger_handler, level=logging.ERROR)
        self.__set_color_handle(console_handle)

        if level == 'info':
            self.__logger.info(message)
        elif level == 'debug':
            self.__logger.debug(message)
        elif level == 'warning':
            self.__logger.warning(message)
        elif level == 'error':
            self.__logger.error(message)
        elif level == 'critical':
            self.__logger.critical(message)

        self.__logger.removeHandler(all_logger_handler)  # 避免日志输出重复问题
        self.__logger.removeHandler(error_logger_handler)
        self.__logger.removeHandler(console_handle)

        self.__close_handler(all_logger_handler)  # 关闭handler
        self.__close_handler(error_logger_handler)

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)

    def critical(self, message):
        self.__console('critical', message)

log = HandleLog()