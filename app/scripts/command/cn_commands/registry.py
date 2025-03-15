from functools import wraps

from ...schemas.response import JSONResponse, ResponseDict
from ...schemas import KokomiUser
from ...logs import logging


class CommandRegistry:
    """ 管理指令注册和解析 """
    COMMANDS = {}  # 存储指令 -> (处理函数, 所需权限)

    @staticmethod
    def command_handler(command, permission_level: int):
        """ 注册指令，并支持自定义参数解析 """
        def decorator(func):
            CommandRegistry.COMMANDS[command] = (func, permission_level)
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
    async def parse_input(cls, user: KokomiUser, user_input: str) -> ResponseDict:
        """ 解析用户输入，匹配指令 """
        parts = user_input.strip().split(maxsplit=1)  # 分割指令和参数
        command = parts[0]
        logging.debug(f'Extract keywords： {command}')
        raw_args = parts[1] if len(parts) > 1 else ""
        if command in cls.COMMANDS:
            handle_func, permission_level = cls.COMMANDS[command]
            if user.basic.level not in permission_level:
                # 用户权限不足
                if len(permission_level) == 1 and permission_level[0] == 1:
                    # 先判断是否为仅限root指令
                    return JSONResponse.API_10001_RootRequired
                else:
                    # 需要Root或者Admin权限
                    return JSONResponse.API_10002_AdminOrRootRequired
            callback_func, extra_kwargs = await handle_func(user=user, raw_args=raw_args)
            # 返回值为None表示参数解析失败，返回{}表示解析成功，但没有数据
            if not callback_func and not extra_kwargs:
                return JSONResponse.API_10005_InvalidArgs
            elif not callback_func and extra_kwargs:
                return extra_kwargs
            else:
                return cls.return_data(callback_func, extra_kwargs)

        return JSONResponse.API_10004_CommandNotFound
