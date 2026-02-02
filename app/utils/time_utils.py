import time
from functools import wraps
from datetime import datetime, timezone



class TimeUtils:
    """时间相关工具函数集合"""
    @staticmethod
    def timestamp() -> int:
        """
        获取当前 UTC 时间戳（秒）
        """
        return int(datetime.now(timezone.utc).timestamp())

    @staticmethod
    def timestamp_ms() -> int:
        """
        获取当前 UTC 时间戳（毫秒）
        """
        return int(datetime.now(timezone.utc).timestamp() * 1000)
    
    @staticmethod
    def now_iso() -> str:
        """
        获取指定时区的当前时间（ISO 8601 格式，默认当前时区）
        """
        return datetime.now().isoformat(timespec="seconds")
    
    @staticmethod
    def fromtimestamp(timestamp: int, strftime: str = "%Y-%m-%d %H:%M:%S"):
        return datetime.fromtimestamp(timestamp).strftime(strftime)