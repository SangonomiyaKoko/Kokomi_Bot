# 具体的指令处理函数

from ...resources import (
    test
)

def handle_test(raw_args: str):
    """测试
    
    包含指令：
        - /test [test_msg]
    """
    test_msg = raw_args.strip()
    if test_msg == '' or test_msg == None:
        test_msg = '123456789'
    return test.main(), {'test_msg': test_msg}
