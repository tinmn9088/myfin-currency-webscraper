from cli import ArgumentService
from myfin import MyfinService

settings = ArgumentService.get_settings()

print('Running with settings:', vars(settings))

# download HTML
download_path = MyfinService.download_html(settings.link)

# parse exchange rates
exchange_rates = MyfinService.parse_html(download_path)

# load data to Google Sheet
