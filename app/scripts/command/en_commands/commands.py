from .registry import CommandRegistry
from .handlers import (
    handel_cls,
    handle_test,
    handle_bind,
    handle_basic,
    handle_lang,
    handle_algo
)

# 注册指令
commands = [
    ("/test", [0, 1], False, handle_test),
    ("/cls", [0, 1], False, handel_cls),
    # ("/link", [0, 1, 2], False, handle_bind),
    # ("/basic", [0, 1, 2], True, handle_basic),
    # ("/lang", [0, 1, 2], False, handle_lang),
    # ("/algo", [0, 1, 2], False, handle_algo),
]

for cmd, perm, bind, func in commands:
    CommandRegistry.command_handler(cmd, permission_level=perm, requires_binding=bind)(func)
