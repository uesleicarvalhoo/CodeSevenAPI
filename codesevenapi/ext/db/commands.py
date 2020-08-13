from . import auth
from codesevenapi.ext.db import db
from codesevenapi.ext.db.models import News, Author, User
from werkzeug.security import generate_password_hash, check_password_hash


def create_db():
    db.create_all()


def delete_all():
    db.drop_all()


def validate_user(username, password):
    return User.query.filter(username=username, password=check_password_hash(password))


def get_all_new():
    return News.query.all()


def create_new(title: str, text: str, author_id: str):
    new = News(title=title, text=text, author_id=author_id)

    db.session.add(new)
    db.session.commit()

    return new


def get_new(id: int):
    return News.query.filter_by(id=id).first()


def delete_new(id: int):
    new = News.query.filter_by(id=id).first()

    if new is not None:
        new_data = new.to_dict()
        db.session.delete(new)
        db.session.commit()

        return new_data


def update_new(new_id, title=None, text=None, author_id=None):
    new = News.query.filter_by(id=new_id).first()

    if new is not None:
        if title is not None:
            new.title = title

        if text is not None:
            new.text = text

        if author_id is not None:
            new.author_id = author_id

        db.session.commit()

        return new


def get_all_author():
    return Author.query.all()


def create_author(name: str):
    author = Author(name=name)
    db.session.add(author)
    db.session.commit()

    return author


def get_author(id: int):
    return Author.query.filter_by(id=id).first()


def delete_author(id: int):
    author = Author.query.filter_by(id=id).first()

    if author is not None:
        author_data = author.to_dict()

        db.session.query(Author).filter_by(author_id=id).delete()
        db.session.delete(author)
        db.session.commit()

        return author_data


def update_author(author_id, name=None):
    author = Author.query.filter_by(id=author_id).first()

    if author is not None:
        if name is not None:
            author.name = name

        db.session.commit()

        return author


def create_user(username, password, admin=False):
    user = User(username=username.lower(), password=generate_password_hash(password), admin=admin)
    db.session.add(user)
    db.session.commit()

    return user


def get_user(user_id):
    return User.query.filter_by(id=user_id).first()


def update_user(user_id, password=None, admin=None):
    user = User.query.filter_by(id=user_id).first()

    if user is not None:
        if password is not None:
            user.password = generate_password_hash(password)

        if admin is not None:
            user.admin = admin

        db.session.commit()

        return user


def delete_user(user_id: int):
    user = User.query.filter_by(id=user_id).first()

    if user is not None:
        user_data = user.to_dict()

        db.session.delete(user)
        db.session.commit()

        return user_data


def get_all_user():
    return User.query.all()
