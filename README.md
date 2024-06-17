# Myfin webscraper

Parse _USD exchange rates_ from **Myfin** and load data to **Google Sheet**.

## Launch

Required dependencies:

```
argparse beautifulsoup4 requests google-api-python-client google-auth-httplib2 google-auth-oauthlib gspread
```

Put Google API credentials in _credentials.json_.

Run:

`python run.py <link> <sheet_id>`
