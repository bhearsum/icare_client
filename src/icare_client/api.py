from typing import Dict, Union

import requests
from requests.auth import HTTPBasicAuth

LAYOUT_DATE_FIELDS: Dict[str, Union[str, None]] = {
    "childAttendanceMobile": "dateIn",
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
    # Also no way to query by date - entries are only kept for one day
    "roomMealChangeMobile": None,
    # daily activities are here, but not "special interests"
    "roomProgramDailyActivityMobile": "effectiveDate",
}

LAYOUT_CHILD_ID_FIELDS: Dict[str, str] = {
    "childAttendanceMobile": "childID",
}

LAYOUT_ROOM_ID_FIELDS: Dict[str, str] = {
    # This is a long ID not the short one we get from roomProgramDailyActivityMobile
    # We probably to translate the short id to the long somewhere else first...
    "roomMealChangeMobile": "???",
    "roomProgramDailyActivityMobile": "roomID",
}


def login(session: requests.Session, server: str, username: str, password: str) -> str:
    url = f"{server}/fmi/data/vLatest/databases/iCareMobileAccess/sessions"
    r = session.post(url, auth=HTTPBasicAuth(username, password), json={})
    r.raise_for_status()

    return r.json()["response"]["token"]


def get_child_id(session: requests.Session, server: str, username: str, child_name: str) -> int:
    url = (
        f"{server}/fmi/data/vLatest/databases/iCareMobileAccess/layouts/childBasicWithMobileAppUserAccountMobile/_find"
    )
    params = {
        "query": [
            {
                "mobileAppUserAccount::accountName": username,
            }
        ],
    }

    r = session.post(url, json=params)
    r.raise_for_status()

    for child in r.json()["response"]["data"]:
        if child["fieldData"]["firstName"] == child_name:
            return int(child["fieldData"]["childID"])

    raise ValueError("Couldn't find child id")
