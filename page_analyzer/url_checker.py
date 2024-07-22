from collections import namedtuple

import requests
from bs4 import BeautifulSoup


def get_page_content(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return

    return parse_html(response)


def parse_html(response):
    PageContent = namedtuple('PageContent',
                             ['h1', 'title', 'description', 'status_code'])
    soup = BeautifulSoup(response.text, 'html.parser')
    h1 = soup.find('h1').text
    title = soup.find('title').text
    description = soup.find('meta', attrs={'name': 'description'})['content']

    return PageContent(
        h1=h1[:255] if h1 else '',
        title=title[:255] if title else '',
        description=description[:255] if description else '',
        status_code=response.status_code
    )
