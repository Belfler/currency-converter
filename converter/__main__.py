from converter.app import configure_server
from converter.utils import create_argparser


if __name__ == '__main__':
    args = create_argparser().parse_args()
    server = configure_server(args.host, args.port)
    server.serve_forever()
