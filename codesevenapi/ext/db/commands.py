from codesevenapi.ext.db import db


def create_db():
    """Create database."""
    db.create_all()


def delete_all():
    """Cleans database."""
    db.drop_all()
