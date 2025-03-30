from .registry import CommandRegistry
from .handlers import handle_test

# 注册指令
CommandRegistry.command_handler("/test", permission_level=[0,1,2])(func=handle_test)
