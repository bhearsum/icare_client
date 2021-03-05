from typing import Dict

import click
import requests

from .api import LAYOUT_DATE_FIELDS, login


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
    "schedule": "childEatingMobile",
    "sendmore": "childItemRequestMobile",
    "sleep": "childSleepMobile",
}

@click.group()
@click.option("--server", required=True, type=str)
@click.option("--username", required=True, type=str)
@click.option("--password", required=True, type=str)
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
        layout_names = [l["name"] for l in r.json()["response"]["layouts"][0]["folderLayoutNames"]]
        print("\n".join(layout_names))


@cli.command()
@click.pass_context
@click.option("--child-id", required=True, type=int)
@click.option("--date", type=str)
@click.option("--limit", type=int)
@click.option("--output-format", type=click.Choice(["text", "html"]), default="text")
@click.argument("section", nargs=-1)
def download(ctx, child_id, date, limit, output_format, section):
    server = ctx.obj["server"]
    username = ctx.obj["username"]
    password = ctx.obj["password"]

    with requests.session() as session:
        for s in section:
            print(f"Section: {s}")
            layout = LAYOUT_ALIASES[s]
            token = login(session, server, username, password)
            session.headers["Authorization"] = f"Bearer {token}"
            url = f"{server}/fmi/data/vLatest/databases/iCareMobileAccess/layouts/{layout}/_find"
            params = {
                "query": [{
                    "child::childId": child_id,
                }],
            }
            if date:
                date_field = LAYOUT_DATE_FIELDS[layout]
                if date_field:
                    params["query"][0][date_field] = date
            if limit:
                params["limit"] = limit
            r = session.post(url, json=params)
            if r.json()["messages"][0]["code"] == "0":
                if output_format == "text":
                    import pprint
                    pprint.pprint(r.json())
                else:
                    print("and here's where i'd output html")
            else:
                print("Got error when downloading records")
