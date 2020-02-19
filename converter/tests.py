import json
import unittest
import threading
from http.client import responses
from http.server import HTTPServer
from urllib.error import HTTPError

from converter.app import *
from converter.handlers import *
from converter.utils import *


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
    server: HTTPServer
    host: str = 'localhost'
    port: int = 8000

    @classmethod
    def setUpClass(cls) -> None:
        cls.server = configure_server(Dispatcher, cls.host, cls.port)
        thread = threading.Thread(target=cls.server.serve_forever)
        thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()

    def test_request_no_query_string(self) -> None:
        response = request_url(f'http://{self.host}:{self.port}')
        data = json.loads(response)
        self.assertEqual(data['base_currency'], 'USD')
        self.assertEqual(data['target_currency'], 'RUB')
        self.assertIn('rate', data)

    def test_request_eur_to_chf_with_amount(self) -> None:
        base = 'EUR'
        target = 'CHF'
        amount = 100
        response = request_url(f'http://{self.host}:{self.port}?base={base}&target={target}&amount={amount}')
        data = json.loads(response)
        self.assertEqual(data['base_currency'], base)
        self.assertEqual(data['target_currency'], target)
        self.assertIn('rate', data)
        self.assertIn('amount_in_base_currency', data)
        self.assertEqual(data['amount_in_base_currency'], amount)
        self.assertIn('amount_in_target_currency', data)

    def test_request_not_existing_page(self) -> None:
        with self.assertRaises(HTTPError):
            request_url(f'http://{self.host}:{self.port}/index.php')


class TestUtils(unittest.TestCase):
    def test_configure_server(self) -> None:
        server_address = ('0.0.0.0', 7575)
        server = configure_server(Dispatcher, *server_address)
        self.assertIs(server.RequestHandlerClass, Dispatcher)
        self.assertEqual(server.server_address, server_address)
        server.socket.close()

    def test_response_with_error(self) -> None:
        expected_result = (404, {'Content-Type': 'application/json'}, json.dumps({'error': responses[404]}))
        actual_result = response_with_error(404)
        self.assertEqual(expected_result, actual_result)

        msg = 'Remote server is unavailable'
        expected_result = (424, {'Content-Type': 'application/json'}, json.dumps({'error': msg}))
        actual_result = response_with_error(424, error_msg=msg)
        self.assertEqual(expected_result, actual_result)


if __name__ == '__main__':
    unittest.main()
