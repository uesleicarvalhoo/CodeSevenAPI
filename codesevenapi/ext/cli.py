import click
from codesevenapi.ext.db.commands import create_db

def init_app(app):
    app.cli.add_command(app.cli.command()(create_db))
