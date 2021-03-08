import pprint
from typing import Any, Callable, Dict, List, Optional, Union

from jinja2 import Environment, PackageLoader, select_autoescape

SECTION_FORMATS: Dict[str, str] = {
    "diaper": "* {when}: {type}",
    "food": """{meal}: {menu}
* {amount}
* Milk: {milkAmount} {milkUnits}
* Water: {waterAmount} {waterUnits}
""",
    "sleep": """* Duration: {length}
* Woke Up At: {wakeTime}
* Comments: {comments}""",
}

SectionData = Union[str, Dict[str, Union[str, List[str]]]]

SECTION_SORTS: Dict[str, SectionData] = {
    "diaper": "when",
    "food": {
        "key": "meal",
        "order": ["Breakfast", "Lunch", "Snack 1", "Snack 2"],
    },
}


def section_key(section: str) -> Callable:
    sortBy = SECTION_SORTS.get(section)

    def get_key(item: dict) -> Optional[Any]:
        if isinstance(sortBy, str):
            return item.get(sortBy)
        elif isinstance(sortBy, dict):
            return sortBy["order"].index(item[sortBy["key"]])
        else:
            return None

    return get_key


def text_output(section_data: Dict[str, SectionData]) -> None:
    for section, data in section_data.items():
        print(f"{section.capitalize()} Information:")
        fmt = SECTION_FORMATS.get(section)
        if fmt:
            for d in sorted(data, key=section_key(section)):
                print(fmt.format(**d))  # type: ignore
        else:
            pprint.pprint(data)

    print()


def html_output(section_data: Dict[str, SectionData], child_name: str, date: str) -> None:
    env = Environment(loader=PackageLoader("icare_client", "templates"), autoescape=select_autoescape(["html"]))
    sorted_section_data = {k: sorted(v, key=section_key(k)) for k, v in section_data.items()}
    print(env.get_template("report.html").render(child_name=child_name, date=date, **sorted_section_data))
