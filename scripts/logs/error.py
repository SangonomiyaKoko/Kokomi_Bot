import os
import time

from scripts.config import LOG_DIR

def write_error_info(
    error_id: str,
    error_type: str,
    error_name: str,
    error_args: str = None,
    error_info: str = None
):
    now_day = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    form_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
    with open(os.path.join(LOG_DIR, f'{now_day}.txt'), "a", encoding="utf-8") as f:
        f.write('-------------------------------------------------------------------------------------------------------------\n')
        f.write(f">Platform:     API\n")
        f.write(f">Error ID:     {error_id}\n")
        f.write(f">Error Type:   {error_type}\n")
        f.write(f">Error Name:   {error_name}\n")
        f.write(f">Error Time:   {form_time}\n")
        f.write(f">Error Info:   \n{error_args}\n{error_info}\n")
        f.write('-------------------------------------------------------------------------------------------------------------\n')
    f.close()