## Currency Converter

[![Python 3.8](https://img.shields.io/badge/python-3.8-brightgreen.svg)](https://www.python.org/downloads/release/python-380/) [![Build Status](https://travis-ci.com/Belfler/currency-converter.svg?branch=master)](https://travis-ci.com/Belfler/currency-converter) [![codecov](https://codecov.io/gh/Belfler/currency-converter/branch/master/graph/badge.svg)](https://codecov.io/gh/Belfler/currency-converter)



HTTP server currency converter. Data is retrieved from https://exchangeratesapi.io/

### How to install
Just clone: `git clone https://github.com/Belfler/currency-converter.git`

### How to use
0) Start tests (optionally): `python -m converter.tests`

1) Start server: `python -m converter [--host HOST] [--port PORT]`

or with Docker: `docker build -t converter . && docker run -d -p 8000:8000 converter`

2) Send HTTP GET request to the home page with query string args:

`base` -- base currency that converter converts from

`target` -- target currency that converter converts to

`amount` -- amount of base currency's money that you want to convert

#### Example

Request: 

    GET /?base=USD&target=RUB&amount=100 HTTP/1.1
    Host: localhost:8000

Response: 

    HTTP/1.1 200 OK
    Content-Type: application/json
    
    {"base_currency": "USD", "target_currency": "RUB", "rate": 63.5412037037, "amount_in_base_currency": 100.0, "amount_in_target_currency": 6354.12037037}
    

