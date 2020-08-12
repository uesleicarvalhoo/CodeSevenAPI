from . import db

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.Unicode)
    text = db.Column('text', db.Unicode)
    author_id = db.Column('author', db.Unicode, db.ForeignKey('author.id'))

    author = db.relationship('Author', foreign_keys=author_id)

    def get_data(self):
        data = {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'author_id': self.author_id
        }

        return data

class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode)

    def get_data(self):
        data = {
            'id': self.id,
            'name': self.name
        }

        return data
