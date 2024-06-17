import gspread
from google.oauth2.service_account import Credentials
from myfin import ExchangeRate


class ExchangeRatesWriter:

    def __init__(self, sheet_id: str):
        '''
        Load creadentials from credentials.json, open spreadsheet by id and get the first worksheet.
        '''

        scopes = [
            'https://www.googleapis.com/auth/spreadsheets'
        ]

        credentials = Credentials.from_service_account_file('credentials.json', scopes=scopes)

        client = gspread.authorize(credentials)

        spreadsheet = client.open_by_key(sheet_id)

        self.worksheet = spreadsheet.get_worksheet(0)

    def __enter__(self) -> None:
        self.worksheet.clear()
        return self

    def insert_header(self, text: str) -> None:
        '''
        Paste text in A1 cell and merge A1:D1 cells.
        '''

        # insert text
        self.worksheet.update(range_name='A1', values=[[text]])

        # position at center and make bold
        self.worksheet.format('A1', {
            'horizontalAlignment': 'CENTER',
            'textFormat': {
                'fontSize': 12,
                'bold': True
            }
        })

        # merge cells
        self.worksheet.merge_cells('A1:D1')

    def insert_usd_input_field(self) -> None:
        '''
        Insert label and input field at A3:B3.
        '''

        self.worksheet.update(range_name='A3:B3', values=[['Кол-во USD:', 1]])

        self.worksheet.format('A3', {
            'horizontalAlignment': 'RIGHT',
            'textFormat': {
                'fontSize': 10,
                'bold': True
            }
        })

        self.worksheet.format('B3', {
            'horizontalAlignment': 'LEFT',
            'backgroundColorStyle': self.get_color(255, 242, 204),
            'textFormat': {
                'fontSize': 10,
                'bold': False
            }
        })

    def insert_exchange_rates(self, exchange_rates: list[ExchangeRate]) -> None:
        '''
        Insert table with header at A5:D5.
        '''

        start_table_row_number = 5
        start_content_row_number = start_table_row_number + 1

        # column names
        values = [['Банк', 'Курс USD', 'Стоимость', 'Разница']]

        for row_number, exchange_rate in enumerate(sorted(exchange_rates, key=lambda r: r.buy_usd), start=start_content_row_number):
            values.append(
                [
                    exchange_rate.bank_name,
                    exchange_rate.buy_usd,
                    f'=B3*(B{row_number})',  # cost
                    f'=B3*(B{row_number}-B{start_content_row_number})',  # difference in cost
                ]
            )

        # send exchange rates
        self.worksheet.update(
            range_name=f'A{start_table_row_number}:D{start_table_row_number + len(values)}',
            values=values,
            value_input_option='USER_ENTERED'  # to prevent escaping formulas
        )

        # format table header
        self.worksheet.format(f'A{start_table_row_number}:D{start_table_row_number}', {
            'horizontalAlignment': 'CENTER',
            'textFormat': {
                'fontSize': 10,
                'bold': True
            }
        })

        # format difference cells
        self.worksheet.format(f'D{start_content_row_number + 1}:D{start_table_row_number + len(values) - 1}', {
            'backgroundColorStyle': self.get_color(244, 204, 204),
            'textFormat': {
                'fontSize': 10,
                'bold': False
            }
        })

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.worksheet.columns_auto_resize(0, 5)

    @staticmethod
    def get_color(red: int, green: int, blue: int):
        return {
            'rgbColor': {
                'red': red / 255,
                'green': green / 255,
                'blue': blue / 255
            }
        }
