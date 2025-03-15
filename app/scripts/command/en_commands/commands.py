from .registry import CommandRegistry
from .handlers import (
    handle_bind,
    handle_test,
    handle_basic
)

# 注册指令
CommandRegistry.command_handler("/test", permission_level=[0,1])(func=handle_test)
CommandRegistry.command_handler("/link", permission_level=[0,1,2])(func=handle_bind)
CommandRegistry.command_handler("/basic", permission_level=[0,1,2])(func=handle_basic)
