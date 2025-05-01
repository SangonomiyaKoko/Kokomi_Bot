from .registry import CommandRegistry
from .handlers import (
    handler_cls,
    handler_test,
    handler_bind,
    handler_help,
    handler_basic,
    handler_lang,
    handler_algo,
    handler_content,
    handler_theme,
    handler_admin,
    handler_alias,
    handler_card
)

# 注册指令
commands = [
    ("/test", [0, 1, 2], False, handler_test),
    ("/cls", [0, 1], False, handler_cls),
    ("/admin", [0, 1], False, handler_admin),
    ("/link", [0, 1, 2], False, handler_bind),
    ("/help", [0, 1, 2], False, handler_help),
    ("/stat", [0, 1, 2], True, handler_basic),
    ("/lang", [0, 1, 2], False, handler_lang),
    ("/algo", [0, 1, 2], False, handler_algo),
    ("/mode", [0, 1, 2], False, handler_content),
    ("/theme", [0, 1, 2], False, handler_theme),
    ("/alias", [0, 1, 2], False, handler_alias),
    ("/card", [0, 1, 2], True, handler_card)
]

for cmd, perm, bind, func in commands:
    CommandRegistry.command_handler(cmd, permission_level=perm, requires_binding=bind)(func)
