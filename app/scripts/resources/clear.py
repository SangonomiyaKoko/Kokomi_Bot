
import os
import glob

from ..config import OUTPUT_DIR
from ..logs import ExceptionLogger
from ..schemas import KokomiUser, JSONResponse

@ExceptionLogger.handle_program_exception_async
async def main(
    user: KokomiUser
) -> dict:
    # 查找文件夹下所有 .png 和 .webp 文件
    png_files = glob.glob(os.path.join(OUTPUT_DIR, "*.png"))
    webp_files = glob.glob(os.path.join(OUTPUT_DIR, "*.webp"))
    # 合并文件列表
    all_files = png_files + webp_files
    # 删除文件
    for file in all_files:
        try:
            os.remove(file)
        except Exception as e:
            pass
    return JSONResponse.API_10006_ClearCacheSuccess