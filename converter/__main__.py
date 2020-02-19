from converter.utils import create_argparser, configure_server
from converter.app import Dispatcher


if __name__ == '__main__':
    args = create_argparser().parse_args()
    server = configure_server(Dispatcher, args.host, args.port)
    server.serve_forever()
