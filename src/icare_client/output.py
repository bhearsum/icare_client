import os
import os.path
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

# I can't figure out the proper value for the Dict keys
# so Any will have to do for now
SectionData = Union[str, Dict[Any, Union[str, List[str]]]]

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
            return ""

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


def html_output(section_data: Dict[str, SectionData], output_dir: str, child_name: str, date: str) -> None:
    output_dir = os.path.join(os.path.abspath(os.path.expanduser(output_dir)), date.replace("/", "-"))
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    env = Environment(loader=PackageLoader("icare_client", "templates"), autoescape=select_autoescape(["html"]))
    sorted_section_data = {k: sorted(v, key=section_key(k)) for k, v in section_data.items()}

    picture_links = []
    if sorted_section_data.get("pictures"):
        for i, data in enumerate(sorted_section_data["pictures"]):
            with open(os.path.join(output_dir, f"{i}.jpg"), "wb+") as fp:
                fp.write(data["image"])
                picture_links.append(f"{i}.jpg")

        # won't be used; no point in passing it
        del sorted_section_data["pictures"]

    with open(os.path.join(output_dir, "report.html"), "w+") as f:
        f.write(
            env.get_template("report.html").render(
                child_name=child_name, date=date, pictures=picture_links, **sorted_section_data
            )
        )
