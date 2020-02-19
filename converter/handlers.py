import json
import urllib.parse
from urllib.error import URLError, HTTPError

from converter.exceptions import RemoteServerError
from converter.utils import request_url, response_with_error

__all__ = ['USDHandler', 'not_found_handler']


class USDHandler:
    def __call__(self, environ: dict, url_args: dict) -> tuple:
        self.environ = environ
        self.url_args = url_args
        method = self.environ['REQUEST_METHOD'].lower()
        if hasattr(self, method):
            return getattr(self, method)()
        else:
            return response_with_error(405)

    @staticmethod
    def get_rate() -> float:
        try:
            response = request_url('https://api.exchangeratesapi.io/latest?base=USD&symbols=RUB')
        except (URLError, HTTPError) as e:
            raise RemoteServerError(e)

        data = json.loads(response)

        if 'error' in data:
            raise RemoteServerError(data['error'])

        rate = data['rates']['RUB']
        return rate

    def get(self) -> tuple:
        try:
            rate = self.get_rate()
        except RemoteServerError as e:
            return response_with_error(424, str(e))

        content = {
            'base_currency': 'USD',
            'target_currency': 'RUB',
            'rate': rate,
        }
        qs = urllib.parse.parse_qs(self.environ['QUERY_STRING'])
        if 'amount' in qs:
            amount_in_base_currency = float(qs['amount'][0])
            amount_in_target_currency = rate * amount_in_base_currency
            content.update({
                'amount_in_base_currency': amount_in_base_currency,
                'amount_in_target_currency': amount_in_target_currency,
            })
        return 200, {'Content-Type': 'application/json'}, json.dumps(content)


def not_found_handler(environ: dict, url_args: dict) -> tuple:
    return response_with_error(404)
