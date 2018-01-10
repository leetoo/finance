import json

import requests

from finance.models import Granularity
from finance.providers import AssetValueProvider


class Yahoo(AssetValueProvider):
    """Fetches and parses financial data from Yahoo Finance."""

    def __init__(self):
        pass

    def get_url(self, symbol):
        """Returns a URL to be fetched.

        :param symbol: A symbol of a security (e.g., NVDA, MSFT)
        """
        return 'https://query1.finance.yahoo.com/v8/finance/chart/{0}'

    def asset_values(self, symbol, start_time, end_time,
                     granularity=Granularity.day):
        mappings = {
            Granularity.day: self.fetch_daily_data,
            Granularity.min: self.fetch_data_by_minutes,
        }

        try:
            rows = mappings[granularity](symbol, start_time, end_time)
        except KeyError:
            raise NotImplementedError

        return self.filter_empty_rows(rows)

    # NOTE: 'Data by day' would keep the name consistent, but 'daily data'
    # sounds more natural.
    def fetch_daily_data(self, symbol, start_time, end_time):
        url = self.get_url(symbol)

        params = {
            'symbol': symbol,
            'period1': int(start_time.timestamp()),
            'period2': int(end_time.timestamp()),
            'interval': '1d',
            'includePrePost': 'true',
            'events': 'div%7Csplit%7Cearn',
            'corsDomain': 'finance.yahoo.com',
        }
        resp = requests.get(url, params=params)
        rows = self.parse_chart_data(resp.text)

        return rows

    def fetch_data_by_minutes(self, symbol, start_time, end_time):
        url = self.get_url(symbol)

        params = {
            'symbol': symbol,
            'period1': int(start_time.timestamp()),
            'period2': int(end_time.timestamp()),
            'interval': '1m',
            'includePrePost': 'true',
            'events': 'div%7Csplit%7Cearn',
            'corsDomain': 'finance.yahoo.com',
        }
        resp = requests.get(url, params=params)
        rows = self.parse_chart_data(resp.text)

        return rows

    def parse_chart_data(self, raw_json):
        """Parses Yahoo Finance chart data.

        See some examples if necessary:
        - sample-data/yahoo_finance_msft_1m.json
        - sample-data/yahoo_finance_nvda_1d.json
        """
        parsed = json.loads(raw_json)

        timestamps = parsed['chart']['result'][0]['timestamp']
        quote = parsed['chart']['result'][0]['indicators']['quote'][0]

        keys = ['open', 'high', 'low', 'close', 'volume']
        cols = [timestamps] + [quote[k] for k in keys]

        # Transposition from column-wise data to row-wise data
        return zip(*cols)

    def filter_empty_rows(self, rows):
        for row in rows:
            if all([c is not None for c in row]):
                yield row
