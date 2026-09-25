import requests
import re

SERVER_HEADERS = [
    "Server",
    "X-Powered-By",
    "X-AspNet-Version",
    "X-AspNetMvc-Version",
    "X-Generator",
    "X-Runtime",
    "X-Backend-Server",
    "X-Served-By",
    "X-Cache",
    "Via",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",
]


def get_redirects(response):
    return [
        {
            "url": redirect.url,
            "status_code": redirect.status_code,
            "location": redirect.headers.get("Location"),
        }
        for redirect in response.history
    ]


def get_security_headers(headers):
    return {
        header: headers.get(header)
        for header in SECURITY_HEADERS
        if headers.get(header) is not None
    }


def get_server_info(headers):
    return {
        header: headers.get(header)
        for header in SERVER_HEADERS
    }


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
            "server": get_server_info(response.headers),
            "security_headers": get_security_headers(response.headers),
            "redirects": get_redirects(response),
            "headers": response.headers
        }
    except requests.RequestException:
        return None
