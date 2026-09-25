import requests


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
            "headers": response.headers
        }
    except requests.RequestException:
        return None
