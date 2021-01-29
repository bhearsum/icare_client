import click
import requests

from .api import login


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
@click.argument("layout")
def download(ctx, child_id, layout):
    server = ctx.obj["server"]
    username = ctx.obj["username"]
    password = ctx.obj["password"]

    with requests.session() as session:
        token = login(session, server, username, password)
        session.headers["Authorization"] = f"Bearer {token}"
        url = f"{server}/fmi/data/vLatest/databases/iCareMobileAccess/layouts/{layout}/_find"
        params = {
            "query": [{
                "child::childId": child_id,
            }]
        }
        r = session.post(url, json=params)
        r.raise_for_status()
        import pprint
        pprint.pprint(r.json())
