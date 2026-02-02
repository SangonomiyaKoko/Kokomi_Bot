import uuid
import traceback

from .error_log import write_error_info
from app.response import JSONResponse


class ExceptionLogger:
    @staticmethod
    def handle_program_exception_async(func):
        "负责异步程序异常信息的捕获"
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                error_id = str(uuid.uuid4())
                write_error_info(
                    error_id = error_id,
                    error_type = 'ProgramError',
                    error_name = str(type(e).__name__),
                    error_args = str(args) + str(kwargs),
                    error_info = traceback.format_exc()
                )
                return JSONResponse.get_error_response(6000,'ProgramError',error_id)
        return wrapper

    @staticmethod
    def handle_program_exception_sync(func):
        "负责异步程序异常信息的捕获"
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                error_id = str(uuid.uuid4())
                write_error_info(
                    error_id = error_id,
                    error_type = 'ProgramError',
                    error_name = str(type(e).__name__),
                    error_args = str(args) + str(kwargs),
                    error_info = traceback.format_exc()
                )
                return JSONResponse.get_error_response(6000,'ProgramError',error_id)
        return wrapper