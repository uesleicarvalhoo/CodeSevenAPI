from . import db
from .models import News, Author

def create_db():
    db.create_all()

def add_new(title: str, text: str, author_id: str):
    new = News(title=title, text=text, author_id=author_id)

    db.session.add(new)
    db.session.commit()

    return new.get_data()

def get_new(id: int):
    response = {
        'id': id,
        'title': 'titulo',
        'text': 'texto'
    }

    return response

def get_all_author():
    return [author.get_data() for author in Author.query.all()]

def new_author(name):
    author = Author(name=name)
    db.session.add(author)
    db.session.commit()

    return author.get_data()
