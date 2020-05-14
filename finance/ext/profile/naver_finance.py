from bs4 import BeautifulSoup
import requests

from finance.ext.profile.base import BaseProfile


class NaverProfile(BaseProfile):
    """
    Example profile source: https://finance.naver.com/item/coinfo.nhn?code=063170
    """

    def __init__(self, symbol: str):
        super(NaverProfile, self).__init__(symbol)
        self.soup = None

    @property
    def url(self):
        return f"https://finance.naver.com/item/coinfo.nhn?code={self.symbol}"

    def fetch(self):
        resp = requests.get(self.url)
        return resp.text

    def parse(self, raw: str):
        """This could easily break along the way. We need a more robust way
        to parse the raw HTML.
        """
        self.soup = BeautifulSoup(raw)

        self.name = self.soup.select("div.wrap_company h2 a")[0].text

        current_price_raw = self.soup.select("div.today p.no_today span.blind")[0].text
        self.current_price = int(current_price_raw.replace(",", ""))

        rows = self.soup.select("table[summary='시가총액 정보'] tr")
        assert len(rows) == 4, f"Expected rows: 4, actual: {len(rows)}"

        outstanding_shares_raw = rows[2].select("td")[0].text
        self.outstanding_shares = int(outstanding_shares_raw.replace(",", ""))


def fetch_naver_profile(symbol: str):
    profile = NaverProfile(symbol)
    profile.parse(profile.fetch())

    return profile
