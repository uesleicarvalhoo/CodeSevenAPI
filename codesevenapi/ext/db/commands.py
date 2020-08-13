from codesevenapi.ext.db import db
from codesevenapi.ext.db.models import News, Author, User
from werkzeug.security import generate_password_hash, check_password_hash


def create_db():
    db.create_all()


def delete_all():
    db.drop_all()


def validate_user(username, password):
    return User.query.filter(username=username, password=check_password_hash(password))
