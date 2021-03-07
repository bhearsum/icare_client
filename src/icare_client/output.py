import pprint
from typing import Callable, Dict, List, Union

from jinja2 import Environment, PackageLoader, select_autoescape

SECTION_FORMATS: Dict[str, str] = {
    "diaper": "* {when}: {type}",
    "food": """{meal}: {menu}
* {amount}
* Milk: {milkAmount} {milkUnits}
* Water: {waterAmount} {waterUnits}
""",
    # TODO: Improve time formatting (arrow.humanize for length, probably)
    "sleep": """* Duration: {length}
* Woke Up At: {wakeTime}
* Comments: {comments}""",
}

SECTION_SORTS: Dict[str, Union[str, List[str]]] = {
    "diaper": "when",
    "food": {
        "key": "meal",
        "order": ["Breakfast", "Lunch", "Snack 1", "Snack 2"],
    },
}


def section_key(section: str) -> Callable:
    sortBy = SECTION_SORTS.get(section)

    def get_key(item: dict) -> str:
        if isinstance(sortBy, str):
            return item.get(sortBy)
        elif isinstance(sortBy, dict):
            return sortBy["order"].index(item[sortBy["key"]])
        else:
            return None

    return get_key


def text_output(section_data: Dict[str, dict]) -> None:
    for section, data in section_data.items():
        print(f"{section.capitalize()} Information:")
        fmt = SECTION_FORMATS.get(section)
        if fmt:
            for d in sorted(data, key=section_key(section)):
                print(fmt.format(**d))
        else:
            pprint.pprint(data)

    print()


def html_output(section_data: Dict[str, dict]) -> None:
    env = Environment(loader=PackageLoader("icare_client", "templates"), autoescape=select_autoescape(["html"]))
    print(env.get_template("report.html").render(childName="Kieran", date="2020-02-02", **section_data))
