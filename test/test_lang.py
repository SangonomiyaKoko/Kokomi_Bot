from functools import wraps

class SelectFunc:
    """ 指令解析与注册管理 """
    COMMANDS = {}  # 存储指令 -> (处理函数, 解析方法)

    @staticmethod
    def command_handler(command, parser=None):
        """ 注册指令，并支持自定义参数解析 """
        def decorator(func):
            SelectFunc.COMMANDS[command] = (func, parser)  # 绑定指令到解析方法
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
    def parse_input(cls, user_input: str):
        """ 解析用户输入，匹配对应的指令和解析参数 """
        parts = user_input.strip().split(maxsplit=1)  # 拆分指令和参数
        command = parts[0]  # 获取指令
        raw_args = parts[1] if len(parts) > 1 else ""  # 剩余内容作为参数

        if command in cls.COMMANDS:
            callback_func, parser = cls.COMMANDS[command]  # 获取对应的处理函数和解析方法
            
            # 使用自定义解析器解析参数
            extra_kwargs = parser(raw_args) if parser else {"raw_args": raw_args}

            return cls.return_data(callback_func, extra_kwargs)

        return {
            'status': 'error',
            'code': 4004,
            'message': 'Command not found',
            'data': {}
        }

# ============================
#       参数解析方法
# ============================
def bind_parser(args: str):
    """ 解析 /bind 指令的参数，例如 `/bind Player123` """
    return {"name": args.strip()} if args else {}

def stats_parser(args: str):
    """ 解析 /stats 指令的参数，例如 `/stats Player123 damage kills` """
    parts = args.strip().split()
    if len(parts) < 2:
        return {"error": "Invalid stats format"}
    return {"player": parts[0], "stats": parts[1:]}

# ============================
#       指令注册
# ============================
@SelectFunc.command_handler("/bind", parser=bind_parser)
def bind_account(name: str):
    return f"Account {name} bound successfully!"

@SelectFunc.command_handler("/stats", parser=stats_parser)
def get_player_stats(player: str, stats: list):
    return f"Fetching {', '.join(stats)} for player {player}."

# ============================
#        测试代码
# ============================
if __name__ == "__main__":
    commands = ["/bind Player123", "/stats Player123 damage kills", "/unknown"]

    for cmd in commands:
        result = SelectFunc.parse_input(cmd)
        print(result)
