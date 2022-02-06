
import re
from locale import currency
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from django.conf import settings

from utils import get_money_dict


class ZapCrawler:

    def __init__(self, url) -> None:
        self.url = url

    def get_data(self):
        html = self._get_page()
        self.soup = BeautifulSoup(html, 'html.parser')
        price = self._get_price()
        return {
            'currency': price.get('currency'),
            'price': price.get('value'),
            'condominium': self._get_condominium().get('value'),
            'iptu': self._get_iptu().get('value')
        }

    def _get_page(self):
        request = Request(self.url)
        request.add_header('User-Agent', settings.CRAWLER_USER_AGENT)
        response = urlopen(request)
        return response

    def _get_price(self):
        try:
            price = self.soup.find_all('li', 'price__item--main')[0]
            for desc in price.find('strong').descendants:
                if 'R$' in desc:
                    return get_money_dict(desc.strip())
        except Exception:
            return {}

    def _get_condominium(self):
        try:
            condominium = self.soup.find('li', 'condominium').find('span', 'price__value').string
            return get_money_dict(condominium)
        except Exception:
            return {}

    def _get_iptu(self):
        try:
            iptu = self.soup.find('li', 'iptu').find('span', 'price__value').string
            return get_money_dict(iptu)
        except Exception:
            return {}
