import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class ExchangeRate:
    bank_name: str
    buy_usd: float


class MyfinService:

    DOWNLOADS_DIRECTORY = '.content'

    HEADER_SELECTOR = '.top-content__inline-title'

    BANK_ROW_SELECTOR = '.currencies-courses__row-main'

    @classmethod
    def parse_html(cls, link: str) -> tuple[str, list[ExchangeRate]]:
        '''
        Parse header and exchange rates.
        '''

        # errors parameter is required to prevent UnicodeDecodeError
        with requests.get(link) as response:
            response.encoding = 'utf-8'
            html = BeautifulSoup(response.text, 'html.parser')

        header = html.select_one(cls.HEADER_SELECTOR).text.strip()

        # get <tbody>
        bank_rows = html.select(cls.BANK_ROW_SELECTOR)

        exchange_rates = []

        for bank_row in bank_rows:

            # bank name
            current_element = bank_row.find_next('td')
            bank_name = current_element.text.strip()

            if not bank_name:
                continue

            # sell usd (skip)
            current_element = current_element.find_next_sibling('td')

            # buy usd
            current_element = current_element.find_next_sibling('td')
            buy_usd = float(current_element.text)

            exchange_rates.append(
                ExchangeRate(bank_name, buy_usd)
            )

        return (header, exchange_rates)
