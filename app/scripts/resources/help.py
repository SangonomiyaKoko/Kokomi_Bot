import os
from ..logs import ExceptionLogger
from ..image import (
    ImageHandler
)
from ..schemas import KokomiUser, JSONResponse
from ..config import ASSETS_DIR


@ExceptionLogger.handle_program_exception_async
async def help(user: KokomiUser) -> dict:
    help_png_path = os.path.join(ASSETS_DIR, 'docs', user.local.content, user.local.language, 'help.png')
    if os.path.exists(help_png_path):
        res_img = ImageHandler.open_image(help_png_path)
        result = ImageHandler.save_image(res_img)
    else:
        result = JSONResponse.API_10008_ImageResourceMissing
    return result
