import os
import json
import httpx

from ..logs import logging
from ..config import api_settings
from ..logs import ExceptionLogger
from ..common import TimeFormat

class BaseAPI:
    @ExceptionLogger.handle_network_exception_async
    @TimeFormat.cost_time_async('API request completed')
    async def get(path: str, params: dict) -> dict:
        "实现get请求"
        base_url = api_settings.API_URL + path
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
                timeout=api_settings.REQUEST_TIMEOUT
            )
            request_code = res.status_code
            logging.debug(f"GET {url} {request_code}")
            result = res.json()
        if request_code == 200:
            return result
        else:
            res.raise_for_status()

    @ExceptionLogger.handle_network_exception_async
    async def post(path: str, params: dict, body: dict) -> dict:
        "实现post请求"
        base_url = api_settings.API_URL + path
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
                timeout=api_settings.REQUEST_TIMEOUT
            )
            request_code = res.status_code
            logging.debug(f"POST {url} {request_code}")
            result = res.json()
        if request_code == 200:
            return result
        else:
            res.raise_for_status()

    @ExceptionLogger.handle_network_exception_async
    async def put(path: str, params: dict, body: dict) -> dict:
        "实现put请求"
        base_url = api_settings.API_URL + path
        if params == {}:
            url = '{}'.format(base_url)
        else:
            url = '{}?{}'.format(base_url, '&'.join(['{}={}'.format(key, value) for key, value in params.items()]))
        headers = {
            'accept': 'application/json'
        }
        async with httpx.AsyncClient() as client:
            res = await client.put(
                url=url, 
                headers=headers,
                json=body,
                timeout=api_settings.REQUEST_TIMEOUT
            )
            request_code = res.status_code
            logging.debug(f"PUT {url} {request_code}")
            result = res.json()
        if request_code == 200:
            return result
        else:
            res.raise_for_status()