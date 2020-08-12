from flask_restful import Api
from .resources import News, Author

api = Api()
api.add_resource(News, '/noticias')
api.add_resource(Author, '/autor')

def init_app(app):
    api.init_app(app)
