import json
import urllib.parse
from typing import Dict, List, Any
from urllib.error import URLError, HTTPError

from converter.exceptions import RemoteServerError
from converter.utils import request_url, response_with_error

__all__ = ['ConverterHandler', 'not_found_handler']


class ConverterHandler:
    def __call__(self, environ: dict, url_args: dict) -> tuple:
        self.environ: Dict[str, Any] = environ
        self.url_args: Dict[str, str] = url_args
        self.qs_args: Dict[str, List[str]] = urllib.parse.parse_qs(self.environ['QUERY_STRING'])
        method: str = self.environ['REQUEST_METHOD'].lower()
        if hasattr(self, method):
            return getattr(self, method)()
        else:
            return response_with_error(405)

    @staticmethod
    def get_rate(base: str = 'USD', target: str = 'RUB') -> float:
        try:
            response: str = request_url(f'https://api.exchangeratesapi.io/latest?base={base}&symbols={target}')
        except (URLError, HTTPError) as e:
            raise RemoteServerError(e)

        data = json.loads(response)

        if 'error' in data:
            raise RemoteServerError(data['error'])

        rate = float(data['rates'][target])
        return rate

    def get(self) -> tuple:
        base_currency: str = self.qs_args.get('base', ['USD'])[0]
        target_currency: str = self.qs_args.get('target', ['RUB'])[0]
        try:
            rate: float = self.get_rate(base_currency, target_currency)
        except RemoteServerError as e:
            return response_with_error(424, str(e))

        content = {
            'base_currency': base_currency,
            'target_currency': target_currency,
            'rate': rate,
        }

        if 'amount' in self.qs_args:
            amount_in_base_currency = float(self.qs_args['amount'][0])
            amount_in_target_currency = rate * amount_in_base_currency
            content.update({
                'amount_in_base_currency': amount_in_base_currency,
                'amount_in_target_currency': amount_in_target_currency,
            })
        return 200, {'Content-Type': 'application/json'}, json.dumps(content)


def not_found_handler(environ: dict, url_args: dict) -> tuple:
    return response_with_error(404)
