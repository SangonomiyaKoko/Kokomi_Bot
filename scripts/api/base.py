import httpx

from ..config.setting import APIConfig
from ..logs.exception import ExceptionLogger

class BaseAPI:
    @ExceptionLogger.handle_network_exception_async
    async def get(path: str, params: dict) -> dict:
        "实现get请求"
        base_url = APIConfig.API_URL + path
        if params == {}:
            url = '{}'.format(base_url)
        else:
            url = '{}?{}'.format(base_url, '&'.join(['{}={}'.format(key, value) for key, value in params.items()]))
        headers = {
            'accept': 'application/json'
        }
        async with httpx.AsyncClient() as client:
            res = await client.get(
                url=url, 
                headers=headers,
                timeout=APIConfig.REQUEST_TIMEOUT
            )
            request_code = res.status_code
            result = res.json()
        if request_code == 200:
            return result
        else:
            res.raise_for_status()

    @ExceptionLogger.handle_network_exception_async
    async def post(path: str, params: dict, body: dict) -> dict:
        "实现post请求"
        base_url = APIConfig.API_URL + path
        if params == {}:
            url = '{}'.format(base_url)
        else:
            url = '{}?{}'.format(base_url, '&'.join(['{}={}'.format(key, value) for key, value in params.items()]))
        headers = {
            'accept': 'application/json'
        }
        async with httpx.AsyncClient() as client:
            res = await client.post(
                url=url, 
                headers=headers,
                json=body,
                timeout=APIConfig.REQUEST_TIMEOUT
            )
            request_code = res.status_code
            result = res.json()
        if request_code == 200:
            return result
        else:
            res.raise_for_status()