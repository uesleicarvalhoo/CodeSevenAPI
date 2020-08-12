import json

from flask_restful import Resource
from flask import request
from sqlalchemy.exc import OperationalError

from codesevenapi.ext.db.commands import add_new, get_new, get_all_author, new_author

class News(Resource):
    def get(self):
        return [new.get_data() for new in News.query.all()]

    def post(self):
        data = json.loads(request.data)
        response = dict()

        try:
            author_id = data['author_id']
            title = data['title']
            text = data['text']

            new = add_new(title, text, author_id)

        except KeyError:
            response = {
                'message': 'Informe todos os parametros: ["title", "text" e "author_id"]'
            }

        except OperationalError:
            response = {
                'message': 'Não foi possível cadastrar a noticia, verifique os parametros informados e tente novamente.'
            }

        else:
            response = {
                'message': 'Noticia cadastrada com sucesso!',
                'id': new.id,
                'author': new.author_id,
                'title': new.title,
                'text': new.text
            }

        return response


class Author(Resource):
    def get(self):
        return get_all_author()

    def post(self):
        data = json.loads(request.data)
        response = dict()

        try:
            name = data['name']
            author = new_author(name)

        except KeyError:
            response = {
                'message': 'Preencha todos os parametros: ["name"]'
            }

        except OperationalError:
            response = {
                'message': 'Não foi possível cadastrar o Autor, verifique os parametros informados e tente novamente.'
            }

        else:
            response = {
                'message': 'Autor cadastrado com sucesso!',
                'author': author
            }

        return response
