import requests
import re


def get_title(html):
    match = re.search(
        r"<title[^>]*>(.*?)</title>",
        html,
        re.IGNORECASE | re.DOTALL
    )
    if match:
        return match.group(1).strip()
    else:
        return None


def get_http_info(url):
    try:
        response = requests.get(
            url,
            timeout=5,
            allow_redirects=True
        )
        return {
            "url": response.url,
            "status_code": response.status_code,
            "title": get_title(response.text),
            "headers": response.headers
        }
    except requests.RequestException:
        return None
