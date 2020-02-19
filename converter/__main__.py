from argparse import Namespace
from http.server import HTTPServer

from converter.utils import create_argparser, configure_server
from converter.app import Dispatcher


if __name__ == '__main__':
    args: Namespace = create_argparser().parse_args()
    server: HTTPServer = configure_server(Dispatcher, args.host, args.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
