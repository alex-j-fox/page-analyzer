from urllib.parse import urlparse


def normalize_url(url_value: str) -> str:
    parsed_url = urlparse(url_value)
    return f'{parsed_url.scheme}://{parsed_url.hostname}'


def is_exists_url_name(normalized_url: str, urls: list) -> bool:
    return any(normalized_url in _ for _ in urls)
