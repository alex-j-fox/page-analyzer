from typing import List, Tuple, Any, Union
from urllib.parse import urlparse


def normalize_url(url_value: str) -> str:
    """Normalize a given URL by removing any path or query parameters.

    :param url_value: The URL to normalize.
    :type url_value: str
    :return: The normalized URL.
    :rtype: str
    """
    parsed_url = urlparse(url_value)
    return f'{parsed_url.scheme}://{parsed_url.hostname}'


def is_exists_url_name(normalized_url: str,
                       urls_list: List[Tuple[Union[str, Any], ...]]) -> bool:
    """Check if a normalized URL exists in a list of URLs.

     :param normalized_url: The normalized URL to search for.
     :type normalized_url: str
     :param urls_list: A list of tuples containing normalized URLs and their
      corresponding names.
     :type urls_list: (List[Tuple[str, str]]):
     :return: True if the normalized URL exists in the list, False otherwise.
     :rtype: bool
    """
    return any(normalized_url in _ for _ in urls_list)
