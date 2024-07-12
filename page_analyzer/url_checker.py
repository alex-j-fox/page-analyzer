import requests


def check_url_accessibility(url: str) -> requests.Response or None:
    try:
        response = requests.get(url)
        if not response.raise_for_status():
            return response
    except requests.exceptions.RequestException:
        return None
