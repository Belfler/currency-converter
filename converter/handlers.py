import json
import urllib.parse
from typing import Dict, List, Any
from urllib.error import URLError, HTTPError

from converter.exceptions import RemoteServerError
from converter.typing import HandlerResponse
from converter.utils import request_url, response_with_error

__all__ = ['ConverterHandler', 'not_found_handler']


class ConverterHandler:
    environ: Dict[str, Any]
    url_args: Dict[str, str]
    qs_args: Dict[str, List[str]]

    def __call__(self, environ: Dict[str, Any], url_args: Dict[str, str]) -> HandlerResponse:
        self.environ = environ
        self.url_args = url_args
        self.qs_args = urllib.parse.parse_qs(self.environ['QUERY_STRING'])
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

        data: Dict[str, Any] = json.loads(response)

        if 'error' in data:
            raise RemoteServerError(data['error'])

        rate: float = float(data['rates'][target])
        return rate

    def get(self) -> HandlerResponse:
        base_currency: str = self.qs_args.get('base', ['USD'])[0]
        target_currency: str = self.qs_args.get('target', ['RUB'])[0]
        try:
            rate: float = self.get_rate(base_currency, target_currency)
        except RemoteServerError as e:
            return response_with_error(424, str(e))

        content: Dict[str, Any] = {
            'base_currency': base_currency,
            'target_currency': target_currency,
            'rate': rate,
        }

        if 'amount' in self.qs_args:
            amount_in_base_currency: float = float(self.qs_args['amount'][0])
            amount_in_target_currency: float = rate * amount_in_base_currency
            content.update({
                'amount_in_base_currency': amount_in_base_currency,
                'amount_in_target_currency': amount_in_target_currency,
            })
        return 200, {'Content-Type': 'application/json'}, json.dumps(content)


def not_found_handler(environ: Dict[str, Any], url_args: Dict[str, str]) -> HandlerResponse:
    return response_with_error(404)
