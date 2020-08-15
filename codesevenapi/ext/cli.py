import click
from sqlalchemy.exc import IntegrityError, OperationalError
from tabulate import tabulate

from codesevenapi.ext.db.commands import create_db, delete_all
from codesevenapi.ext.db.models import Author, News, User


def init_app(app):
    app.cli.add_command(app.cli.command()(create_db))
    app.cli.add_command(app.cli.command()(delete_all))
    app.cli.add_command(app.cli.command()(add_user))
    app.cli.add_command(app.cli.command()(delete_user))
    app.cli.add_command(app.cli.command()(list_all_users))
    app.cli.add_command(app.cli.command()(list_all_news))
    app.cli.add_command(app.cli.command()(list_all_authors))


@click.option("--username", "-u")
@click.option("--password", "-p")
@click.option("--admin", "-a", is_flag=True, default=False)
def add_user(username: str, password: str, admin: bool):
    """Create a User, flag --admin to create a administrator """
    try:
        User.create(username, password, admin)

    except IntegrityError:
        click.echo(f'O usuario "{username}" já existe.')

    except OperationalError:
        click.echo("Não foi possível cadastrar o usuario, erro desconhecido.")

    else:
        click.echo(f'Usuario "{username}" cadastrado com sucesso!')


@click.option("--username", "-u")
def delete_user(username: str):
    "Delete a user by username"
    User.query.filter_by(username=username).first().delete()


def list_all_users():
    """List all Users: ID, Username, IsAdmin."""
    click.echo(
        tabulate(
            [[user.id, user.username, user.is_admin] for user in User.query.all()],
            headers=["ID", "Username", "Admin"],
            tablefmt="orgtbl",
        )
    )


def list_all_news():
    "List all News: ID, Title, Text, Author, Create at."
    click.echo(
        tabulate(
            [
                [new.id, new.title, new.text, new.author.name, new.create_at]
                for new in News.query.all()
            ],
            headers=["ID", "Title", "Text", "Author", "Create at"],
            tablefmt="orgtbl",
        )
    )


def list_all_authors():
    """List all Authors: ID, Name."""
    click.echo(
        tabulate(
            [[author.id, author.name] for author in Author.query.all()],
            headers=["ID", "Name"],
            tablefmt="orgtbl",
        )
    )
