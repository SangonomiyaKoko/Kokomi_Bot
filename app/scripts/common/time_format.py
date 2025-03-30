import time
from datetime import datetime, timezone

from ..config import bot_settings
from ..logs import logging

# 定义不同区域的 UTC 偏移量
REGION_UTC_LIST = {
    1: 8,  # 亚服：UTC+8
    2: 1,  # 欧服：UTC+1
    3: -7, # 美服：UTC-7
    4: 3,  # 莱服：UTC+3
    5: 8   # 国服：UTC+8
}

class TimeFormat:
    """
    提供时间格式化和计算的工具方法。
    包括：获取当前时间、根据区域ID转换时间戳、计算函数执行时间等功能。
    """

    @staticmethod
    def get_datetime_now() -> str:
        """
        获取当前的 UTC 时间并格式化为字符串。

        返回：
            str: 格式化的时间字符串，例如 "2024-12-11T08:30:15.123456+00:00"。
        """
        utc_time_with_zone = str(datetime.now(timezone.utc))
        return utc_time_with_zone[:19].replace(' ', 'T') + utc_time_with_zone[26:]

    @staticmethod
    def get_strftime(region_id: int, timestamp: int, format: str = '%Y%m%d') -> str:
        """
        获取指定区域对应时区的时间，并将其格式化为字符串。

        参数：
            region_id (int): 区域 ID，根据该 ID 获取对应的时区偏移。
            timestamp (int): 要转换的时间戳。
            format (str): 输出的时间格式，默认为 '%Y%m%d'。

        返回：
            str: 转换后的时间字符串。
        """
        time_zone = REGION_UTC_LIST.get(region_id)
        if time_zone is None:
            raise ValueError(f"无效的区域 ID: {region_id}")
        return time.strftime(format, time.gmtime(timestamp + time_zone * 3600))

    @staticmethod
    def cost_time_sync(message: str):
        """
        装饰器：计算同步函数的执行时间，仅在调试模式下生效。

        参数：
            message (str): 日志消息，描述函数的名称或功能。

        返回：
            decorator: 装饰器函数。
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                if bot_settings.LOG_LEVEL == 'debug':
                    start_time = time.time()
                    result = func(*args, **kwargs)
                    end_time = time.time()
                    logging.debug(f"{message}, cost: {round(end_time - start_time, 2)}s")
                    return result
                else:
                    return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def cost_time_async(message: str):
        """
        装饰器：计算异步函数的执行时间，仅在调试模式下生效。

        参数：
            message (str): 日志消息，描述函数的名称或功能。

        返回：
            decorator: 装饰器函数。
        """
        def decorator(func):
            async def wrapper(*args, **kwargs):
                if bot_settings.LOG_LEVEL == 'debug':
                    start_time = time.time()
                    result = await func(*args, **kwargs)
                    end_time = time.time()
                    logging.debug(f"{message}, cost: {round(end_time - start_time, 2)}s")
                    return result
                else:
                    return await func(*args, **kwargs)
            return wrapper
        return decorator
