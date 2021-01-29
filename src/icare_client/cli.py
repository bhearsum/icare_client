import click
import requests

from .api import login


@click.group()
@click.option("--server", required=True, type=str)
@click.option("--username", required=True, type=str)
@click.option("--password", required=True, type=str)
@click.option("--child-id", required=True, type=int)
@click.pass_context
def cli(ctx, server, username, password, child_id):
    ctx.ensure_object(dict)
    ctx.obj["server"] = server
    ctx.obj["username"] = username
    ctx.obj["password"] = password
    ctx.obj["child_id"] = child_id


@cli.command()
@click.pass_context
def download(ctx):
    server = ctx.obj["server"]
    username = ctx.obj["username"]
    password = ctx.obj["password"]
    child_id = ctx.obj["child_id"]

    with requests.session() as session:
        token = login(session, server, username, password)
        session.headers["Authorization"] = f"Bearer {token}"
