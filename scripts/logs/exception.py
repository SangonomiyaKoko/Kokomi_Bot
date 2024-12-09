import uuid
import traceback

import httpx
import sqlite3

from .error import write_error_info

class ExceptionType:
    program = 'Program'
    network = 'Network'
    database = 'Database'

class NerworkExceptionName:
    connect_timeout = 'ConnectTimeout'
    read_timeout = 'ReadTimeout'
    request_timeout = 'RequestTimeout'
    network_error = 'NetworkError'
    connect_error = 'ConnectError'
    read_error = 'ReadError'

class DatabaseExceptionName:
    programming_error = 'ProgrammingError'
    operational_error = 'OperationalError'
    integrity_error = 'IntegrityError'
    database_error = 'DatabaseError'

def generate_error_id():
    return str(uuid.uuid4())

class ExceptionLogger:
    @staticmethod
    def handle_program_exception_async(func):
        "负责异步程序异常信息的捕获"
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                error_id = generate_error_id()
                write_error_info(
                    error_id = error_id,
                    error_type = ExceptionType.program,
                    error_name = str(type(e).__name__),
                    error_args = str(args) + str(kwargs),
                    error_info = traceback.format_exc()
                )
                return {'status': 'error','code': 5000,'message': 'ProgramError','data': {'error_id': error_id}}
        return wrapper
    
    @staticmethod
    def handle_program_exception_sync(func):
        "负责同步程序异常信息的捕获"
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                error_id = generate_error_id()
                write_error_info(
                    error_id = error_id,
                    error_type = ExceptionType.program,
                    error_name = str(type(e).__name__),
                    error_args = str(args) + str(kwargs),
                    error_info = traceback.format_exc()
                )
                return {'status': 'error','code': 5000,'message': 'ProgramError','data': {'error_id': error_id}}
        return wrapper
    
    @staticmethod
    def handle_database_exception_sync(func):
        "负责同步数据库 sqlite3 的异常捕获"
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except sqlite3.ProgrammingError as e:
                error_id = generate_error_id()
                write_error_info(
                    error_id = error_id,
                    error_type = ExceptionType.database,
                    error_name = DatabaseExceptionName.programming_error,
                    error_args = str(args) + str(kwargs),
                    error_info = f'ERROR_{e.args[0]}\n' + str(e.args[1]) + f'\n{traceback.format_exc()}'
                )
                return {'status': 'error','code': 3001,'message': 'DatabaseError','data': {'error_id': error_id}}
            except sqlite3.OperationalError as e:
                error_id = generate_error_id()
                write_error_info(
                    error_id = error_id,
                    error_type = ExceptionType.database,
                    error_name = DatabaseExceptionName.operational_error,
                    error_args = str(args) + str(kwargs),
                    error_info = f'ERROR_{e.args[0]}\n' + str(e.args[1]) + f'\n{traceback.format_exc()}'
                )
                return {'status': 'error','code': 3002,'message': 'DatabaseError','data': {'error_id': error_id}}
            except sqlite3.IntegrityError as e:
                error_id = generate_error_id()
                write_error_info(
                    error_id = error_id,
                    error_type = ExceptionType.database,
                    error_name = DatabaseExceptionName.integrity_error,
                    error_args = str(args) + str(kwargs),
                    error_info = f'ERROR_{e.args[0]}\n' + str(e.args[1]) + f'\n{traceback.format_exc()}'
                )
                return {'status': 'error','code': 3003,'message': 'DatabaseError','data': {'error_id': error_id}}
            except sqlite3.DatabaseError as e:
                error_id = generate_error_id()
                write_error_info(
                    error_id = error_id,
                    error_type = ExceptionType.database,
                    error_name = DatabaseExceptionName.database_error,
                    error_args = str(args) + str(kwargs),
                    error_info = f'ERROR_{e.args[0]}\n' + str(e.args[1]) + f'\n{traceback.format_exc()}'
                )
                return {'status': 'error','code': 3000,'message': 'DatabaseError','data': {'error_id': error_id}}
            except Exception as e:
                error_id = generate_error_id()
                write_error_info(
                    error_id = error_id,
                    error_type = ExceptionType.program,
                    error_name = str(type(e).__name__),
                    error_info = traceback.format_exc()
                )
                return {'status': 'error','code': 5000,'message': 'ProgramError','data': {'error_id': error_id}}
        return wrapper
    
    @staticmethod
    def handle_network_exception_async(func):
        "负责异步网络请求 httpx 的异常捕获"
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                return result
            except httpx.ConnectTimeout:
                error_id = generate_error_id()
                write_error_info(
                    error_id = error_id,
                    error_type = ExceptionType.network,
                    error_name = NerworkExceptionName.connect_timeout,
                    error_args = str(args) + str(kwargs)
                )
                return {'status': 'error','code': 2001,'message': 'NetworkError','data': {'error_id': error_id}}
            except httpx.ReadTimeout:
                error_id = generate_error_id()
                write_error_info(
                    error_id = error_id,
                    error_type = ExceptionType.network,
                    error_name = NerworkExceptionName.read_timeout,
                    error_args = str(args) + str(kwargs)
                )
                return {'status': 'error','code': 2002,'message': 'NetworkError','data': {'error_id': error_id}}
            except httpx.TimeoutException:
                error_id = generate_error_id()
                write_error_info(
                    error_id = error_id,
                    error_type = ExceptionType.network,
                    error_name = NerworkExceptionName.request_timeout,
                    error_args = str(args) + str(kwargs)
                )
                return {'status': 'error','code': 2003,'message': 'NetworkError','data': {'error_id': error_id}}
            except httpx.ConnectError:
                error_id = generate_error_id()
                write_error_info(
                    error_id = error_id,
                    error_type = ExceptionType.network,
                    error_name = NerworkExceptionName.connect_error,
                    error_args = str(args) + str(kwargs)
                )
                return {'status': 'error','code': 2004,'message': 'NetworkError','data': {'error_id': error_id}}
            except httpx.ReadError:
                error_id = generate_error_id()
                write_error_info(
                    error_id = error_id,
                    error_type = ExceptionType.network,
                    error_name = NerworkExceptionName.read_error,
                    error_args = str(args) + str(kwargs)
                )
                return {'status': 'error','code': 2005,'message': 'NetworkError','data': {'error_id': error_id}}
            except httpx.HTTPStatusError as e:
                error_id = generate_error_id()
                write_error_info(
                    error_id = error_id,
                    error_type = ExceptionType.network,
                    error_name = NerworkExceptionName.network_error,
                    error_args = str(args) + str(kwargs),
                    error_info = f'StatusCode: {e.response.status_code}'
                )
                return {'status': 'error','code': 2000,'message': 'NetworkError','data': {'error_id': error_id}}
            except Exception as e:
                error_id = generate_error_id()
                write_error_info(
                    error_id = error_id,
                    error_type = ExceptionType.program,
                    error_name = str(type(e).__name__),
                    error_args = str(args) + str(kwargs),
                    error_info = traceback.format_exc()
                )
                return {'status': 'error','code': 5000,'message': 'ProgramError','data': {'error_id': error_id}}
        return wrapper
    