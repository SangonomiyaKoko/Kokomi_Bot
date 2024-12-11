import time
from datetime import datetime, timezone

from scripts.config import bot_settings
from scripts.logs import logging


REGION_UTC_LIST = {
    1: 8,
    2: 1,
    3: -7,
    4: 3,
    5: 8
}

class TimeFormat:
    def get_datetime_now() -> str:
        "获取图片的创建时间的格式"
        # e.g., "2024-12-11 08:30:15.123456+00:00"
        utc_time_with_zone = datetime.now(timezone.utc)
        return utc_time_with_zone
    
    def get_strftime(region_id: int, timestamp: int, format: str = '%Y%m%d') -> str:
        "获取服务器对应时区的时间"
        time_zone = REGION_UTC_LIST.get(region_id)
        return time.strftime(format, time.gmtime(timestamp + time_zone * 3600))

    def cost_time_sync(message: str):
        def decorator(func):
            # debug模式下获取同步函数的执行时间的装饰器
            def wrapper(*args, **kwargs):
                if bot_settings.LOG_LEVEL == 'debug':
                    start_time = time.time()
                    result = func(*args, **kwargs)
                    end_time = time.time()
                    logging.debug(f"{message}, cost: {round(end_time - start_time,2)}s")
                    return result
                else:
                    result = func(*args, **kwargs)
                    return result
            return wrapper
        return decorator

    def cost_time_async(message: str):
        def decorator(func):
            # debug模式下获取异步函数的执行时间的装饰器
            async def wrapper(*args, **kwargs):
                if bot_settings.LOG_LEVEL == 'debug':
                    start_time = time.time()
                    result = await func(*args, **kwargs)
                    end_time = time.time()
                    logging.debug(f"{message}, cost: {round(end_time - start_time,2)}s")
                    return result
                else:
                    result = func(*args, **kwargs)
                    return result
            return wrapper
        return decorator