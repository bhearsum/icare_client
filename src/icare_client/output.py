import pprint
from typing import Dict


SECTION_FORMATS: Dict[str, str] = {
    "diaper": "* {when}: {type}",

    "food": """{meal}: {menu}
* {amount}
* Milk: {milkAmount} {milkUnits}
* Water: {waterAmount} {waterUnits}""",

    # TODO: Improve time formatting (arrow.humanize for length, probably)
    "sleep": """* Duration: {length}
* Woke Up At: {wakeTime}
* Comments: {comments}""",
}


def text_output(data: dict, section: str) -> None:
    print(f"{section.capitalize()} Information:")
    fmt = SECTION_FORMATS.get(section)
    if fmt:
        for d in data:
            print(fmt.format(**d))
    else:
        pprint.pprint(data)

    print()


def html_output(data: dict, section: str) -> None:
    print("outputting html")
