'''
文件架构

commands/
│── commands.py           # 统一注册指令
│── handlers.py           # 具体的指令处理函数
│── parsers.py            # 解析指令参数的方法
│── registry.py   # 核心指令注册逻辑
'''
from .en_commands.registry import CommandRegistry as EnCommandRegistry
from .cn_commands.registry import CommandRegistry as CnCommandRegistry

from ..schemas import KokomiUser

async def select_func(user: KokomiUser, msg: str):
    if user.local.language == 'cn':
        return await EnCommandRegistry.parse_input(user, msg)
    else:
        return await EnCommandRegistry.parse_input(user, msg)