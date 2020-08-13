import json

from flask_restful import Resource
from flask import request
from sqlalchemy.exc import OperationalError

from codesevenapi.ext.db.commands import (
    get_all_new,
    create_new,
    get_new,
    update_new,
    delete_new,
    get_all_author,
    create_author,
    get_author,
    update_author,
    delete_author,
    get_all_user,
    create_user,
    get_user,
    update_user,
    delete_user,
)


class NewAllResource(Resource):
    def get(self):
        try:
            data = [new.to_dict() for new in get_all_new()]

        except OperationalError:
            response = {"message": "Não foi possível obter a lista com as noticias"}

        else:
            response = data

        return response

    def post(self):
        data = json.loads(request.data)
        status = 200

        try:
            author_id = data["author_id"]
            title = data["title"]
            text = data["text"]

            new = create_new(title, text, author_id)

        except KeyError:
            response = {
                "message": 'Informe todos os parametros: ["title", "text" e "author_id"]'
            }

        except OperationalError:
            response = {
                "message": "Não foi possível cadastrar a noticia, verifique os parametros informados e tente novamente."
            }
        else:
            response = {
                "message": "Noticia cadastrada com sucesso!",
                "data": new.to_dict(),
            }

        return response, 201


class NewResource(Resource):
    def get(self, id):
        try:
            new = get_new(id)

        except OperationalError:
            response = {
                "message": f"Não foi possível localizar a noticia com o ID {id}."
            }

        else:
            if new is None:
                response = {}

            else:
                response = {"data": new.to_dict()}

        return response

    def delete(self, id):
        try:
            new = delete_new(id)

        except OperationalError:
            response = {"message": f"Não foi possível excluir a noticia com o ID {id}"}

        else:
            if new is not None:
                response = {"message": "Noticia excluida com sucesso!", "data": new}

            else:
                response = {
                    "message": f"Não foi possível localizar os dados da noticia com ID {id}"
                }

        return response

    def put(self, id):
        data = json.loads(request.data)

        try:
            title = data.get("title", None)
            text = data.get("text", None)
            author_id = data.get("author_id", None)
            new = update_new(id, title, text, author_id)

        except OperationalError:
            response = {"message": f"Erro ao atualizar dados da Noticia com o ID {id}"}

        else:
            if new is not None:
                response = {
                    "message": "Dados atualizados com sucesso!",
                    "data": new.to_dict(),
                }

            else:
                response = {
                    "message": f"Não foi possível localizar os dados da Noticia com o ID {id}"
                }

        return response


class AuthorAllResource(Resource):
    def get(self):
        try:
            authors = get_all_author()

        except OperationalError:
            response = {"message": "Ocorreu um erro ao extrair a lista de Autores"}

        else:
            response = [author.to_dict() for author in authors]

        return response

    def post(self):
        data = json.loads(request.data)
        status = 200

        try:
            name = data["name"]
            author = create_author(name)

        except KeyError:
            response = {"message": 'Os parametros ["name"] são obrigatorios.'}

        except OperationalError:
            response = {
                "message": "Não foi possível cadastrar o Autor, verifique os parametros informados e tente novamente."
            }

        else:
            status = 201
            response = {
                "message": "Autor cadastrado com sucesso!",
                "data": author.to_dict(),
            }

        return response, status


class AuthorResource(Resource):
    def get(self, id):
        try:
            author = get_author(id)

        except OperationalError:
            response = {"message": f"Não foi possível localizar o Autor com o ID {id}."}

        else:
            if author is None:
                response = {}
            else:
                response = author.to_dict()

        return response

    def delete(self, id):
        try:
            new = delete_author(id)

        except OperationalError:
            response = {"message": f"Não foi possível excluir o Autor com o ID {id}"}

        else:
            if new is not None:
                response = {"message": "Autor excluido com sucesso!", "data": new}
            else:
                response = {
                    "message": f"Não foi possível localizar o Autor com o ID {id}"
                }

        return response

    def put(self, id):
        data = json.loads(request.data)

        try:
            name = data.get("name", None)
            author = update_author(id, name)

        except OperationalError:
            response = {"message": f"Erro ao atualizar dados do Autor com o ID {id}"}

        else:
            if author is not None:
                response = {
                    "message": "Dados atualizados com sucesso!",
                    "data": author.to_dict(),
                }

            else:
                response = {
                    "message": f"Não foi possível localizar os dados do Autor com o ID {id}"
                }

        return response


class UserResource(Resource):
    def get(self, user_id):
        try:
            user = get_user(user_id)

        except OperationalError:
            response = {
                "message": f"Não foi possível localizar o Usuario com o ID {user_id}."
            }

        else:
            if user is None:
                response = {}

            else:
                response = user.to_dict()

        return response

    def put(self, user_id):
        data = json.loads(request.data)

        try:
            password = data.get("password", None)
            admin = data.get("admin", None)
            user = update_user(user_id, password, admin)

        except OperationalError:
            response = {"message": f"Erro ao atualizar dados do Autor com o ID {id}"}

        else:
            if user is not None:
                response = {
                    "message": "Dados atualizados com sucesso!",
                    "data": user.to_dict(),
                }

            else:
                response = {
                    "message": f"Não foi possível localizar os dados do Usuario com o ID {id}"
                }

        return response

    def delete(self, user_id):
        try:
            user = delete_user(user_id)

        except OperationalError:
            response = {"message": f"Não foi possível excluir o Usuario com o ID {id}"}

        else:
            if user is not None:
                response = {"message": "Usuario excluido com sucesso!", "data": user}
            else:
                response = {
                    "message": f"Não foi possível localizar o Usuario com o ID {id}"
                }

        return response


class UserAllResource(Resource):
    def get(self):
        try:
            data = [user.to_dict() for user in get_all_user()]

        except OperationalError:
            response = {"message": "Não foi possível obter a lista de usuarios"}

        else:
            response = data

        return response

    def post(self):
        data = json.loads(request.data)
        status = 200

        try:
            username = data["username"]
            password = data["password"]
            admin = data.get("admin", False)

            user = create_user(username, password, admin)

        except KeyError:
            response = {
                "message": 'Os parametros ["username", "password"] são obrigatorios.'
            }

        except OperationalError:
            response = {
                "message": "Não foi possível cadastrar o Usuario, verifique os parametros informados e tente novamente."
            }

        else:
            status = 201
            response = {
                "message": "Usuario cadastrado com sucesso!",
                "data": user.to_dict(),
            }

        return response, status
