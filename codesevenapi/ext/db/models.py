from . import db


class News(db.Model):
    __tablename__ = "news"
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.Unicode)
    text = db.Column("text", db.Unicode)
    author_id = db.Column("author", db.Unicode, db.ForeignKey("author.id"))

    author = db.relationship("Author", foreign_keys=author_id)

    def __repr__(self):
        return f"<New - {self.title.title()}>"

    def to_dict(self):
        data = {
            "id": self.id,
            "title": self.title,
            "text": self.text,
            "author_id": self.author_id,
        }

        return data


class Author(db.Model):
    __tablename__ = "author"
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.Unicode)

    def __repr__(self):
        return f"<Author - {self.name.title()}>"

    def to_dict(self):
        data = {"id": self.id, "name": self.name}

        return data


class User(db.Model):
    __tablename__ = "user"
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.Unicode, unique=True)
    password = db.Column("password", db.Unicode)
    admin = db.Column("admin", db.Boolean)

    def to_dict(self, password=False):
        data = {
            "id": self.id,
            "username": self.username,
            "admin": self.admin,
        }

        if password:
            data["password"] = self.password

        return data
