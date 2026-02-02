from app.utils import TimeUtils
from app.core import STORAGE_DIR

def write_error_info(
    error_id: str,
    error_type: str,
    error_name: str,
    error_args: str = None,
    error_info: str = None
):
    form_time = TimeUtils.now_iso()
    with open(STORAGE_DIR / f'error/{form_time[0:10]}.txt', "a", encoding="utf-8") as f:
        f.write('-------------------------------------------------------------------------------------------------------------\n')
        f.write(f">Platform:     BOT\n")
        f.write(f">Error ID:     {error_id}\n")
        f.write(f">Error Type:   {error_type}\n")
        f.write(f">Error Name:   {error_name}\n")
        f.write(f">Error Time:   {form_time}\n")
        f.write(f">Error Info:   \n{error_args}\n{error_info}\n")
        f.write('-------------------------------------------------------------------------------------------------------------\n')
    f.close()