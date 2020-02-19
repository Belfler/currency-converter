import re
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

from converter.handlers import *


class Dispatcher(BaseHTTPRequestHandler):
    handlers = {
        r'^/usd/$': USDHandler(),
    }

    def build_environ(self) -> dict:
        parsed_url = urllib.parse.urlparse(self.path)
        environ = {
            'REQUEST_METHOD': self.command,
            'PATH_INFO': parsed_url.path,
            'QUERY_STRING': parsed_url.query,
        }
        return environ

    def resolve_url(self) -> tuple:
        handler = not_found_handler
        url_args = {}

        for url_regexp, i_handler in self.handlers.items():
            match = re.match(url_regexp, self.environ['PATH_INFO'])
            if match:
                url_args = match.groupdict()
                handler = i_handler
                break

        return handler, url_args

    def dispatch(self) -> None:
        self.environ = self.build_environ()
        handler, url_args = self.resolve_url()
        status_code, headers, response_content = handler(self.environ, url_args)

        self.send_response(status_code)
        for header_kw, header_val in headers.items():
            self.send_header(header_kw, header_val)
        self.end_headers()
        self.wfile.write(response_content.encode())

    def do_GET(self) -> None:
        self.dispatch()

    def do_POST(self) -> None:
        self.dispatch()


def configure_server(host: str = 'localhost', port: int = 8000) -> HTTPServer:
    server_address = (host, port)
    server = HTTPServer(server_address, Dispatcher)
    return server
