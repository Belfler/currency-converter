import re
from http.server import BaseHTTPRequestHandler
import urllib.parse
from urllib.parse import ParseResult
from typing import Dict, Tuple, Optional, Any

from converter.handlers import *

from converter.typing import Handler

__all__ = ['Dispatcher']


class Dispatcher(BaseHTTPRequestHandler):
    handlers: Dict[str, Handler] = {
        r'^/$': ConverterHandler(),
    }
    environ: Dict[str, Any]

    def build_environ(self) -> Dict[str, Any]:
        parsed_url: ParseResult = urllib.parse.urlparse(self.path)
        environ: Dict[str, Any] = {
            'REQUEST_METHOD': self.command,
            'PATH_INFO': parsed_url.path,
            'QUERY_STRING': parsed_url.query,
        }
        return environ

    def resolve_url(self) -> Tuple[Handler, Dict[str, str]]:
        handler: Handler = not_found_handler
        url_args: Dict[str, str] = {}

        for url_regexp, i_handler in self.handlers.items():
            match: Optional[re.Match] = re.match(url_regexp, self.environ['PATH_INFO'])
            if match:
                url_args = match.groupdict()
                handler = i_handler
                break

        return handler, url_args

    def dispatch(self) -> None:
        self.environ: Dict[str, Any] = self.build_environ()

        handler: Handler
        url_args: Dict[str, str]
        handler, url_args = self.resolve_url()

        status_code: int
        headers: Dict[str, str]
        response_content: str
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
