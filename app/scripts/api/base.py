import os
import json
import httpx
from typing import Dict

from ..logs import logging
from ..config import api_settings
from ..logs import ExceptionLogger
from ..common import TimeFormat

class BaseAPI:
    """
    BaseAPI 类提供了实现基本 HTTP 请求方法（GET、POST、PUT）的功能。
    每个方法都将记录请求的时间并处理网络异常。
    """

    @ExceptionLogger.handle_network_exception_async
    @TimeFormat.cost_time_async('API request completed')
    async def get(path: str, params: Dict[str, str] = {}) -> Dict:
        """
        执行 GET 请求。

        该方法通过将查询参数附加到基础 URL 来构建完整的 URL。
        它会处理网络异常，并记录请求所花费的时间。

        参数:
            path (str): API 端点路径。
            params (dict): 可选的查询参数字典。默认为空字典。

        返回:
            dict: 返回的响应数据，格式为 JSON。

        异常:
            HTTPStatusError: 如果请求返回错误的状态码。
        """
        base_url = api_settings.API_URL + path
        # 构建带查询参数的 URL
        url = f'{base_url}?{"&".join([f"{key}={value}" for key, value in params.items()])}' if params else base_url
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
    @TimeFormat.cost_time_async('API request completed')
    async def post(path: str, params: Dict[str, str] = {}, body: Dict[str, str] = {}) -> Dict:
        """
        执行 POST 请求。

        该方法将请求体数据作为 JSON 发送，并将查询参数附加到基础 URL。
        它会处理网络异常，并记录请求所花费的时间。

        参数:
            path (str): API 端点路径。
            params (dict): 可选的查询参数字典。默认为空字典。
            body (dict): POST 请求的请求体，将作为 JSON 发送。默认为空字典。

        返回:
            dict: 返回的响应数据，格式为 JSON。

        异常:
            HTTPStatusError: 如果请求返回错误的状态码。
        """
        base_url = api_settings.API_URL + path
        # 构建带查询参数的 URL
        url = f'{base_url}?{"&".join([f"{key}={value}" for key, value in params.items()])}' if params else base_url
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
    @TimeFormat.cost_time_async('API request completed')
    async def put(path: str, params: Dict[str, str] = {}, body: Dict[str, str] = {}) -> Dict:
        """
        执行 PUT 请求。

        该方法将请求体数据作为 JSON 发送，并将查询参数附加到基础 URL。
        它会处理网络异常，并记录请求所花费的时间。

        参数:
            path (str): API 端点路径。
            params (dict): 可选的查询参数字典。默认为空字典。
            body (dict): PUT 请求的请求体，将作为 JSON 发送。默认为空字典。

        返回:
            dict: 返回的响应数据，格式为 JSON。

        异常:
            HTTPStatusError: 如果请求返回错误的状态码。
        """
        base_url = api_settings.API_URL + path
        # 构建带查询参数的 URL
        url = f'{base_url}?{"&".join([f"{key}={value}" for key, value in params.items()])}' if params else base_url
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
