from .registry import CommandRegistry
from .handlers import handle_test

# 注册指令
CommandRegistry.command_handler("/test")(func=handle_test)
