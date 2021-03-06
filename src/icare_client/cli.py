import os
import os.path

import arrow
import click
import requests

from .api import LAYOUT_CHILD_ID_FIELDS, LAYOUT_DATE_FIELDS, get_child_id, login
from .data import LAYOUT_ALIASES, extract_data
from .output import html_output, text_output


@click.group()
@click.option(
    "--server", required=True, type=str, default=lambda: os.environ.get("ICARE_SERVER", "https://lullaboo.myddns.com")
)
@click.option("--username", required=True, type=str, default=lambda: os.environ.get("ICARE_USERNAME", None))
@click.option("--password", required=True, type=str, default=lambda: os.environ.get("ICARE_PASSWORD", None))
@click.pass_context
def cli(ctx, server, username, password):
    ctx.ensure_object(dict)
    ctx.obj["server"] = server
    ctx.obj["username"] = username
    ctx.obj["password"] = password


@cli.command()
@click.pass_context
def layouts(ctx):
    server = ctx.obj["server"]
    username = ctx.obj["username"]
    password = ctx.obj["password"]

    with requests.session() as session:
        token = login(session, server, username, password)
        session.headers["Authorization"] = f"Bearer {token}"
        url = f"{server}/fmi/data/vLatest/databases/iCareMobileAccess/layouts"
        r = session.get(url)
        r.raise_for_status()
        layout_names = [layout["name"] for layout in r.json()["response"]["layouts"][0]["folderLayoutNames"]]
        print("\n".join(layout_names))


@cli.command()
@click.pass_context
@click.argument("section", nargs=-1)
def records(ctx, section):
    server = ctx.obj["server"]
    username = ctx.obj["username"]
    password = ctx.obj["password"]

    with requests.session() as session:
        token = login(session, server, username, password)
        session.headers["Authorization"] = f"Bearer {token}"

        for s in section:
            layout = LAYOUT_ALIASES.get(s, s)
            url = f"{server}/fmi/data/vLatest/databases/iCareMobileAccess/layouts/{layout}/records"
            r = session.get(url)

            import pprint

            pprint.pprint(r.json())
    pass


@cli.command()
@click.pass_context
@click.option("--child-name", required=True, type=str, default=lambda: os.environ.get("ICARE_CHILD_NAME", None))
@click.option("--date", type=str, default="today")
@click.option("--limit", type=int)
@click.option("--force-picture-download", type=bool, default=False)
@click.option(
    "--output-format",
    type=click.Choice(["text", "html"]),
    default=lambda: os.environ.get("ICARE_OUTPUT_FORMAT", "text"),
)
@click.option("--html-dir", type=str, default=".")
@click.argument("section", nargs=-1)
def report(ctx, child_name, date, limit, force_picture_download, output_format, html_dir, section):
    server = ctx.obj["server"]
    username = ctx.obj["username"]
    password = ctx.obj["password"]

    query_date = arrow.now().format("MM/DD/YYYY HH:mm:ss")
    if date == "today":
        date = arrow.now().format("MM/DD/YYYY")

    if html_dir:
        html_dir = os.path.join(os.path.abspath(os.path.expanduser(html_dir)), date.replace("/", "-"))
        if not os.path.isdir(html_dir):
            os.mkdir(html_dir)

    if not section or "all" in section:
        sections = LAYOUT_ALIASES.keys()
    else:
        sections = section

    section_data = {}
    picture_links = []

    with requests.session() as session:
        # First grab the room id, which we'll need for various other queries
        token = login(session, server, username, password)
        session.headers["Authorization"] = f"Bearer {token}"

        child_id = get_child_id(session, server, username, child_name)
        url = f"{server}/fmi/data/vLatest/databases/iCareMobileAccess/layouts/childAttendanceMobile/_find"
        params = {"query": [{"childID": child_id, "dateIn": date}]}
        r = session.post(url, json=params)

        for s in sections:
            # To avoid unnecessary downloading, do not process pictures if
            # any already exist.
            if not force_picture_download and s == "pictures" and os.path.exists(os.path.join(html_dir, "0.jpg")):
                for f in os.listdir(html_dir):
                    if f.endswith(".jpg"):
                        picture_links.append(f)

                continue

            layout = LAYOUT_ALIASES.get(s, s)
            url = f"{server}/fmi/data/vLatest/databases/iCareMobileAccess/layouts/{layout}/_find"
            params = {
                "query": [{}],
            }
            if layout in LAYOUT_CHILD_ID_FIELDS:
                for filter_ in LAYOUT_CHILD_ID_FIELDS.get(layout):
                    params["query"][0][filter_] = child_id
            else:
                params["query"][0]["child::childId"] = child_id

            date_field = LAYOUT_DATE_FIELDS.get(layout)
            if date_field:
                params["query"][0][date_field] = date
            if limit:
                params["limit"] = limit
            r = session.post(url, json=params)
            if r.json()["messages"][0]["code"] == "0":
                section_data[s] = extract_data(r.json(), s)
            else:
                print(f"Got error when downloading records for section '{s}':")
                print(r.json())

    if output_format == "text":
        text_output(section_data)
    else:
        html_output(
            section_data,
            output_dir=html_dir,
            child_name=child_name,
            date=date,
            query_date=query_date,
            picture_links=picture_links,
        )
