import argparse
import json
import urllib.request
from http.client import responses
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Type

__all__ = ['create_argparser', 'request_url', 'configure_server', 'response_with_error']


def create_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Currency Converter')
    parser.add_argument('-H', '--host', dest='host', default='localhost')
    parser.add_argument('-p', '--port', dest='port', type=int, default=8000)
    return parser


def request_url(url: str) -> str:
    response = urllib.request.urlopen(url)
    response = response.read().decode('utf-8')
    return response


def configure_server(handler: Type[BaseHTTPRequestHandler], host: str = 'localhost', port: int = 8000) -> HTTPServer:
    server_address = (host, port)
    server = HTTPServer(server_address, handler)
    return server


def response_with_error(http_code: int, error_msg: str = None) -> tuple:
    if error_msg is None:
        error_msg = responses[http_code]
    return http_code, {'Content-Type': 'application/json'}, json.dumps({'error': error_msg})
