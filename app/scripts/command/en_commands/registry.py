from functools import wraps

from ...common.response import JSONResponse
from ...schemas import KokomiUser
from ...logs import logging


class CommandRegistry:
    """ 管理指令注册和解析 """
    COMMANDS = {}  # 存储指令 -> (处理函数, )

    @staticmethod
    def command_handler(command):
        """ 注册指令，并支持自定义参数解析 """
        def decorator(func):
            CommandRegistry.COMMANDS[command] = (func)
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def return_data(callback_func, extra_kwargs: dict | None):
        """ 统一返回数据格式 """
        return {
            'status': 'ok',
            'code': 1000,
            'message': 'Success',
            'data': {
                'callback_func': callback_func,
                'extra_kwargs': extra_kwargs if extra_kwargs else {}
            }
        }

    @classmethod
    async def parse_input(cls, user: KokomiUser, user_input: str):
        """ 解析用户输入，匹配指令 """
        parts = user_input.strip().split(maxsplit=1)  # 分割指令和参数
        command = parts[0]
        logging.debug(f'Extract keywords： {command}')
        raw_args = parts[1] if len(parts) > 1 else ""
        if command in cls.COMMANDS:
            handle_func = cls.COMMANDS[command]
            callback_func, extra_kwargs = await handle_func(raw_args)
            # 返回值为None表示参数解析失败，返回{}表示解析成功，但没有数据
            if not callback_func and not extra_kwargs:
                return JSONResponse.API_9007_InvaildParams
            elif not callback_func and extra_kwargs:
                return extra_kwargs
            else:
                return cls.return_data(callback_func, extra_kwargs)

        return JSONResponse.API_9002_FuncNotFound
