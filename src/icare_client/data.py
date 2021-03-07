from typing import Dict


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
    "sleep": {
        "comments": ["comments"],
        "length": ["sleepDuration"],
        "wakeTime": ["wakeTimestamp"],
    },
}

SECTION_SORTS: Dict[str, str] = {
    "diaper": "timestampChanged",
    "food": "foo",
}


def extract_data(data: dict, section: str) -> dict:
    extracted = []
    fields = RELEVANT_SECTION_FIELDS.get(section)
    if fields:
        for d in [i["fieldData"] for i in data["response"]["data"]]:
            transformed = {}
            for our_field, their_fields in fields.items():
                their_data = [str(d[f]) for f in their_fields]
                transformed[our_field] = " ".join(their_data)

            extracted.append(transformed)
    else:
        extracted.append(data)

    return extracted
