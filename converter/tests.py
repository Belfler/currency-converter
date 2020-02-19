import json
import os
import unittest
from urllib.error import HTTPError

from converter.app import configure_server
from converter.utils import create_argparser, request_url


class TestArgumentParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = create_argparser()

    def test_parse_host_and_port(self) -> None:
        args = self.parser.parse_args(['--host', '0.0.0.0', '--port', '9999'])
        self.assertEqual(args.host, '0.0.0.0')
        self.assertEqual(args.port, 9999)

    def test_default_host_and_port(self) -> None:
        args = self.parser.parse_args()
        self.assertEqual(args.host, 'localhost')
        self.assertEqual(args.port, 8000)


class TestDispatcher(unittest.TestCase):
    def setUp(self) -> None:
        self.host, self.port = 'localhost', 8000
        self.child_pid = os.fork()
        if self.child_pid == 0:
            server = configure_server()
            server.serve_forever()

    def test_availability(self) -> None:
        response = request_url(f'http://{self.host}:{self.port}/usd/')
        data = json.loads(response)
        self.assertEqual(data['base_currency'], 'USD')
        self.assertEqual(data['target_currency'], 'RUB')
        self.assertIn('rate', data)

    def test_request_not_existing_page(self) -> None:
        with self.assertRaises(HTTPError):
            request_url(f'http://{self.host}:{self.port}/index.php')


if __name__ == '__main__':
    unittest.main()
