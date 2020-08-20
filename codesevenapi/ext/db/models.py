import datetime as dt

from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from . import db


class Author(db.Model):
    __tablename__ = "author"
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.Unicode)

    def __repr__(self):
        return f"<Author - {self.name.title()}>"

    def to_dict(self):
        data = {"id": self.id, "name": self.name}

        return data

    @staticmethod
    def create(name: str):
        author = Author(name=name)
        db.session.add(author)
        db.session.commit()

        return author

    @staticmethod
    def get_all():
        return Author.query.all()

    @staticmethod
    def get_by_id(author_id: int):
        return Author.query.filter(Author.id == author_id).first()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        self.name = kwargs.get("name", self.name)

        db.session.commit()

        return self


class News(db.Model):
    __tablename__ = "news"
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.Unicode)
    text = db.Column("text", db.Unicode)
    create_at = db.Column("create_at", db.DateTime, default=dt.datetime.utcnow)
    create_by = db.Column(
        "create_by", db.Integer, db.ForeignKey("user.id"), nullable=False, index=True
    )

    author_id = db.Column(
        "author",
        db.Integer,
        db.ForeignKey("author.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    author = db.relationship("Author", backref="author")
    user = db.relationship("User", backref="user")

    def __repr__(self):
        return f"<New - ID{self.id}>"

    def to_dict(self):
        data = {
            "id": self.id,
            "title": self.title,
            "text": self.text,
            "author": {
                "id": self.author_id,
                "name": self.author.name
            },
            "create_by": {
                "user_id": self.user.id,
                "user_name": self.user.username
            },
        }

        return data

    @staticmethod
    def create(title: str, text: str, author_id: str, user_id: int):
        if Author.get_by_id(author_id) is not None:
            new = News(title=title, text=text, author_id=author_id, create_by=user_id)
            db.session.add(new)
            db.session.commit()

            return new, 201

        else:
            return f"Não existe nenhum Autor cadastrado com o ID {author_id}", 200

    @staticmethod
    def get_all(title=None, author_name=None):
        query = News.query

        if title is not None:
            query = query.filter(News.title.like(f"%{title}%"))

        if author_name is not None:
            query = query.join(Author, News.author_id == Author.id).filter(
                Author.name.like(f"%{author_name}%")
            )

        return query.all()

    @staticmethod
    def get_by_id(new_id: int):
        return News.query.filter(News.id == new_id).first()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        self.title = kwargs.get("title", self.title)
        self.text = kwargs.get("text", self.text)
        self.author_id = kwargs.get("author_id", self.author_id)

        db.session.commit()

        return self


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.Unicode, unique=True)
    password = db.Column("password", db.Unicode)
    admin = db.Column("admin", db.Boolean)

    def __repr__(self):
        return f"<User - {self.username.title()}>"

    def to_dict(self):
        data = {
            "id": self.id,
            "username": self.username,
            "admin": self.admin,
        }

        return data

    @staticmethod
    def create(username: str, password: str, admin=False):
        user = User(
            username=username, password=generate_password_hash(password), admin=admin
        )

        db.session.add(user)
        db.session.commit()

        return user

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_id(user_id: int):
        return User.query.filter(User.id == user_id).first()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        self.username = kwargs.get("username", self.username)
        self.admin = True if kwargs.get("admin", self.admin) else False

        if "password" in kwargs:
            self.password = generate_password_hash(kwargs.get("password"))

        db.session.commit()

        return self

    @property
    def is_admin(self):
        return self.admin
