from functools import wraps

from ...common.response import JSONResponse


class CommandRegistry:
    """ 管理指令注册和解析 """
    COMMANDS = {}  # 存储指令 -> (处理函数, 解析方法)

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
    def parse_input(cls, user, user_input: str):
        """ 解析用户输入，匹配指令 """
        parts = user_input.strip().split(maxsplit=1)  # 分割指令和参数
        command = parts[0]
        raw_args = parts[1] if len(parts) > 1 else ""

        if command in cls.COMMANDS:
            handle_func = cls.COMMANDS[command]
            callback_func, extra_kwargs = handle_func(raw_args)
            # 返回值为None表示参数解析失败，返回{}表示解析成功，但没有数据
            if not callback_func:
                return JSONResponse.API_9007_InvaildParams
            return cls.return_data(callback_func, extra_kwargs)

        return JSONResponse.API_9002_FuncNotFound
