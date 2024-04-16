import logging
from typing import Any, Callable, Dict, Tuple

import json
import aiohttp
import requests

from fyle_teams_app.libs import logger


logger = logger.get_logger(__name__)
logger.level = logging.INFO


async def http_request(method: str, url: str, headers: Dict = None, **kwargs: Any) -> aiohttp.ClientResponse:
    headers = requests.structures.CaseInsensitiveDict(headers)

    async with aiohttp.ClientSession() as session:
        resp = await session.request(
            method=method,
            url=url,
            headers=headers,
            **kwargs
        )
        logger.info('Request %s %s %s', method, url, resp.status)
        logger.info('Response %s', await resp.text())

        return resp


async def process_data_and_headers(data: Dict, headers: Dict) -> Tuple[Dict, Dict]:
    headers = requests.structures.CaseInsensitiveDict(headers)

    if isinstance(data, dict):
        data = json.dumps(data)
        headers['Content-Type'] = 'application/json'

    return data, headers


async def post(url: str, data: Dict = None, headers: Dict = None, **kwargs: Any) -> Callable:
    data, headers = await process_data_and_headers(data, headers)
    return await http_request('POST', url, headers=headers, data=data, **kwargs)


async def put(url: str, data: Dict = None, headers: Dict = None, **kwargs: Any) -> Callable:
    data, headers = await process_data_and_headers(data, headers)
    return await http_request('PUT', url, headers=headers, data=data, **kwargs)


async def get(url: str, *args: Any, **kwargs: Any) -> Callable:
    kwargs.setdefault('allow_redirects', True)
    return await http_request('GET', url, **kwargs)


async def delete(url: str, *args: Any, **kwargs: Any) -> Callable:
    return await http_request('DELETE', url, **kwargs)
