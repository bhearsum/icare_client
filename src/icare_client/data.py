import base64
from typing import Callable, Dict, List, Union

# maps friendly names that humans can use on the cli
# to entries in LAYOUT_DATE_FIELDS
LAYOUT_ALIASES: Dict[str, str] = {
    "diaper": "childDiaperMobile",
    "food": "childMealItemMobile",
    "illness": "childIllnessBasicMobile",
    "incidents": "childIncidentBasicMobile",
    "pictures": "childImageContainerMobile",
    # I don't know why childEatingMobile has daily routine
    # stuff in it, but it appears to.
    # Also, it returns information for multiple rooms
    # We can't parse this correctly until we know how to
    # associate a childId with a roomId
    # It's available in sleep, but there's probably a
    # better place to get it
    "schedule": "childEatingMobile",
    "sendmore": "childItemRequestMobile",
    "sleep": "childSleepMobile",
}

# for each section, our field name -> icare field name
# notable, one of our fields may be multiple icare fields
RELEVANT_SECTION_FIELDS: Dict[str, Dict[str, list]] = {
    "diaper": {
        "cream": ["creamApplied", "creamType"],
        "when": ["timestampChanged"],
        "type": ["wetOrBM"],
    },
    "food": {
        "amount": ["mealResults"],
        "meal": ["meal::mealDescription"],
        "menu": ["menu"],
        "milkAmount": ["milk"],
        "milkUnits": ["milkUnits"],
        "waterAmount": ["water"],
        "waterUnits": ["waterUnits"],
    },
    "pictures": {
        "image": ["imageBase64"],
    },
    "sleep": {
        "comments": ["comments"],
        "length": ["sleepDuration"],
        "wakeTime": ["wakeTimestamp"],
    },
}

iCareData = Dict[str, Union[str, None]]


def time_to_duration(time: str) -> str:
    parts = time.split(":")
    if len(parts) == 3:
        h = int(parts[0])
        m = int(parts[1])
        s = int(parts[2])
        if h:
            return f"{h} hours, {m} minutes, {s} seconds"
        else:
            return f"{int(m)} minutes, {int(s)} seconds"
    # This is super hacky
    else:
        return "Currently Sleeping"


def base64_to_jpg(data: str) -> bytes:
    return base64.b64decode(data.replace("\r\n", ""))


FIELD_TRANSFORMATIONS: Dict[str, Callable] = {
    "sleepDuration": time_to_duration,
    "imageBase64": base64_to_jpg,
}


def extract_data(data: dict, section: str) -> List[iCareData]:
    extracted: List[iCareData] = []
    fields = RELEVANT_SECTION_FIELDS.get(section)
    if fields:
        for d in [i["fieldData"] for i in data["response"]["data"]]:
            transformed: iCareData = {}
            for our_field, their_fields in fields.items():
                their_data = []
                for tf in their_fields:
                    if d[tf]:
                        if FIELD_TRANSFORMATIONS.get(tf):
                            their_data.append(FIELD_TRANSFORMATIONS[tf](d[tf]))
                        else:
                            their_data.append(str(d[tf]))

                if len(their_data) == 0:
                    transformed[our_field] = None
                elif len(their_data) == 1:
                    transformed[our_field] = their_data[0]
                else:
                    transformed[our_field] = " ".join(their_data)

            extracted.append(transformed)
    else:
        extracted.append(data)

    return extracted
