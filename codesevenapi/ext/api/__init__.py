from flask_restful import Api
from .resources import (
    NewResource,
    NewAllResource,
    AuthorResource,
    AuthorAllResource,
    UserAllResource,
    UserResource,
)

api = Api()
api.add_resource(NewResource, "/noticias/<int:new_id>")
api.add_resource(NewAllResource, "/noticias/")
api.add_resource(AuthorAllResource, "/autores/")
api.add_resource(AuthorResource, "/autores/<int:author_id>")
api.add_resource(UserAllResource, "/usuarios/")
api.add_resource(UserResource, "/usuarios/<int:user_id>")


def init_app(app):
    api.init_app(app)
