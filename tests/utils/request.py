from enum import Enum
from typing import Optional

from requests import Response, request


class RequestMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


def make_request(method: RequestMethod, url: str, data: Optional[dict] = None,
                 headers: Optional[dict] = None) -> Response:
    params = {
        'method': method.value,
        'url': url,
        'data': data,
        'headers': headers,
    }

    print(f'Sending the following request: {params}')
    response = request(**params)
    print(f'Received the following status: {response.status_code}')

    return response
