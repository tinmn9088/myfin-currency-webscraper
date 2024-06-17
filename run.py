from cli import ArgumentService
from myfin import MyfinService
from writer import ExchangeRatesWriter


settings = ArgumentService.get_settings()

print('Running with settings:', vars(settings))

# parse exchange rates
header, exchange_rates = MyfinService.parse_html(settings.link)

print(f'Parsed rows: {len(exchange_rates)}')

with ExchangeRatesWriter(settings.sheet_id) as writer:

    # add header
    print('Inserting header ... ', end='')
    writer.insert_header(header)
    print('Done.')

    # add input field
    print('Inserting input field ... ', end='')
    writer.insert_usd_input_field()
    print('Done.')

    # add exhcange rates
    print('Inserting exchange rates ... ', end='')
    writer.insert_exchange_rates(exchange_rates)
    print('Done.')

print('Finished.')
