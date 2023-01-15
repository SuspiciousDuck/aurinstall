import requests
from bs4 import BeautifulSoup

def get_source(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    if 'aur' in link:
        return soup.select_one(".copy")["href"] if soup.select_one(".copy") is not None else None
    else:
        return link + "download" if '/' in link[-1] else link + "/download"