from argparse import ArgumentParser
from settings import Settings


class ArgumentService:

    @staticmethod
    def get_settings() -> Settings:
        '''
        Read command line arguments.
        '''

        parser = ArgumentParser(
            prog='python run.py',
            description='Parse currency exchange rates from Myfin.'
        )

        # command line arguments
        parser.add_argument('link', help='download link')
        parser.add_argument('sheet_id', help='Google Sheet id')

        namespace = parser.parse_args()

        return Settings(
            namespace.link,
            namespace.sheet_id
        )
