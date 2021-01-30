from typing import Dict

import requests
from requests.auth import HTTPBasicAuth


LAYOUT_DATE_FIELDS: Dict[str, str] = {
    "childDiaperMobile": "dateChanged",
    "childEatingMobile": "effectiveDate",
    "childIllnessBasicMobile": "???",
    # It looks like these are only kept for one day, so there's
    # no way to query by date - we should always retrieve all of them.
    "childImageContainerMobile": None,
    # This is actually date + time; not sure how to handle this yet
    "childIncidentBasicMobile": "timestampOccurred",
    "childItemRequestMobile": "requestDate",
    "childMealItemMobile": "effectiveDate",
    "childSleepMobile": "sleepDate",
}

def login(session: requests.session, server: str, username: str, password: str) -> str:
    url = f"{server}/fmi/data/vLatest/databases/iCareMobileAccess/sessions"
    r = session.post(url, auth=HTTPBasicAuth(username, password), json={})
    r.raise_for_status()

    return r.json()["response"]["token"]
