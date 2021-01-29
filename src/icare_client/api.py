import requests
from requests.auth import HTTPBasicAuth


def login(session: requests.session, server: str, username: str, password: str) -> str:
    url = f"{server}/fmi/data/vLatest/databases/iCareMobileAccess/sessions"
    r = session.post(url, auth=HTTPBasicAuth(username, password), json={})
    r.raise_for_status()

    return r.json()["response"]["token"]
