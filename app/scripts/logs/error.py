import os
import time

from ..config import LOG_DIR

def write_error_info(
    error_id: str,
    error_type: str,
    error_name: str,
    error_args: str = None,
    error_info: str = None
):
    # 获取当前日期和时间
    now_day = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    form_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

    # 构造日志文件路径
    log_dir = os.path.join(LOG_DIR, 'error')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)  # 如果目录不存在，则创建

    # 写入错误日志到指定文件
    log_file = os.path.join(log_dir, f'{now_day}.txt')
    with open(log_file, "a", encoding="utf-8") as f:
        # 写入错误信息格式
        f.write('-------------------------------------------------------------------------------------------------------------\n')
        f.write(f">Platform:     API\n")
        f.write(f">Error ID:     {error_id}\n")
        f.write(f">Error Type:   {error_type}\n")
        f.write(f">Error Name:   {error_name}\n")
        f.write(f">Error Time:   {form_time}\n")
        f.write(f">Error Info:   \n{error_args}\n{error_info}\n")
        f.write('-------------------------------------------------------------------------------------------------------------\n')
