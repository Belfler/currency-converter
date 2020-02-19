import argparse
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Type


def create_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='USD-to-RUB Converter')
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
