import click

from codesevenapi.ext.db.commands import create_db, delete_all


def init_app(app):
    app.cli.add_command(app.cli.command()(create_db))
    app.cli.add_command(app.cli.command()(delete_all))
