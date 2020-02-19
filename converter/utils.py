from argparse import ArgumentParser
import json
import urllib.request
from http.client import responses, HTTPResponse
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Type, Optional, Tuple

from converter.typing import HandlerResponse

__all__ = ['create_argparser', 'request_url', 'configure_server', 'response_with_error']


def create_argparser() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(description='Currency Converter')
    parser.add_argument('-H', '--host', dest='host', default='localhost')
    parser.add_argument('-p', '--port', dest='port', type=int, default=8000)
    return parser


def request_url(url: str) -> str:
    response: HTTPResponse = urllib.request.urlopen(url)
    response: str = response.read().decode('utf-8')
    return response


def configure_server(base_handler: Type[BaseHTTPRequestHandler],
                     host: str = 'localhost',
                     port: int = 8000) -> HTTPServer:
    server_address: Tuple[str, int] = (host, port)
    server: HTTPServer = HTTPServer(server_address, base_handler)
    return server


def response_with_error(http_code: int, error_msg: Optional[str] = None) -> HandlerResponse:
    if error_msg is None:
        error_msg: str = responses[http_code]
    return http_code, {'Content-Type': 'application/json'}, json.dumps({'error': error_msg})
