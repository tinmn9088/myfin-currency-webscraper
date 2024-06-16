import os
import re
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class ExchangeRate:
    bank_name: str
    buy_usd: float
    sell_usd: float


class MyfinService:

    DOWNLOADS_DIRECTORY = '.content'

    BANKS_TABLE_SELECTOR = '.sort_body'

    @staticmethod
    def extract_area(link: str) -> str:
        match = re.match('.*\\/(.+)', link)

        if not match:
            raise ValueError(f'Failed to extract area from link: "{link}"')

        return match.group(1)

    @classmethod
    def download_html(cls, link: str) -> str:
        '''
        Download HTML and return file path.
        '''

        # prepare download file path
        area = cls.extract_area(link)

        base_path = os.path.join(os.getcwd(), cls.DOWNLOADS_DIRECTORY)

        os.makedirs(base_path)

        download_path = os.path.join(base_path, f'{area}.html')

        with open(download_path, 'wb') as download_file, requests.get(link) as response:

            print(f'Downloading from {link}')

            if response.status_code != requests.status_codes.codes['ok']:
                raise ConnectionError(f'Server responded with status code {response.status_code}')

            download_file.write(response.content)

            print(f'Downloaded {os.path.getsize(download_path)} bytes (see at {download_path})')

        return download_path

    @classmethod
    def parse_html(cls, download_path: str) -> list[ExchangeRate]:

        # errors parameter is required to prevent UnicodeDecodeError
        with open(download_path, mode='r', errors='ignore') as html_file:
            html = BeautifulSoup(html_file, 'html.parser')

        # get <tbody>
        banks_tbody = html.select_one(cls.BANKS_TABLE_SELECTOR)

        exchange_rates = []

        for bank_tr in banks_tbody:

            # TODO: process

            pass

        return exchange_rates
