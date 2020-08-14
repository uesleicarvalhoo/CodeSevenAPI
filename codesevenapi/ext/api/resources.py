import json

from flask_restful import Resource
from flask import request
from sqlalchemy.exc import OperationalError, IntegrityError

from codesevenapi.ext.db.models import News, Author, User
from flask_login import login_required, current_user


class NewAllResource(Resource):
    def get(self):
        try:
            data = [new.to_dict() for new in News.get_all()]

        except OperationalError:
            response = {"message": "Não foi possível obter a lista com as noticias"}

        else:
            response = data

        return response

    @login_required
    def post(self):
        data = json.loads(request.data)
        status = 200

        try:
            author_id = data["author_id"]
            title = data["title"]
            text = data["text"]

            new = News.create(title, text, author_id)

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
                "new": new.to_dict(),
            }

        return response, 201


class NewResource(Resource):
    def get(self, new_id: int):
        try:
            new = News.get_by_id(new_id)

        except OperationalError:
            response = {
                "message": f"Não foi possível localizar a noticia com o ID {new_id}."
            }

        else:
            if new is None:
                response = {}

            else:
                response = new.to_dict()

        return response

    @login_required
    def delete(self, new_id: int):
        try:
            new = News.get_by_id(new_id)

            if new is not None:
                new_data = new.to_dict()
                new.delete()
                response = {
                    "message": "Noticia excluida com sucesso!",
                    "new": new_data,
                }

            else:
                response = {
                    "message": f"Não foi possível localizar os dados da noticia com ID {new_id}"
                }

        except OperationalError:
            response = {
                "message": f"Não foi possível excluir a noticia com o ID {new_id}"
            }

        return response

    @login_required
    def put(self, new_id: int):
        data = json.loads(request.data)

        try:
            new = News.get_by_id(new_id)

            if new is not None:
                new.update(data)

                response = {
                    "message": "Dados atualizados com sucesso!",
                    "new": new.to_dict(),
                }

            else:
                response = {
                    "message": f"Não foi possível localizar os dados da Noticia com o ID {new_id}"
                }

        except OperationalError:
            response = {
                "message": f"Erro ao atualizar dados da Noticia com o ID {new_id}"
            }

        return response


class AuthorAllResource(Resource):
    def get(self):
        try:
            authors = Author.get_all()

        except OperationalError:
            response = {"message": "Ocorreu um erro ao extrair a lista de Autores"}

        else:
            response = [author.to_dict() for author in authors]

        return response

    @login_required
    def post(self):
        data = json.loads(request.data)
        status = 200

        try:
            name = data["name"]
            author = Author.create(name=name)

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
                "author": author.to_dict(),
            }

        return response, status


class AuthorResource(Resource):
    def get(self, author_id):
        try:
            author = Author.get_by_id(author_id)

        except OperationalError:
            response = {
                "message": f"Não foi possível localizar o Autor com o ID {author_id}."
            }

        else:
            if author is None:
                response = {}

            else:
                response = author.to_dict()

        return response

    @login_required
    def delete(self, author_id: int):
        try:
            author = Author.get_by_id(author_id)
            if author is not None:
                author_data = author.to_dict()
                author.delete()
                response = {
                    "message": "Autor excluido com sucesso!",
                    "author": author_data,
                }

            else:
                response = {
                    "message": f"Não foi possível localizar o Autor com o ID {author_id}"
                }

        except OperationalError:
            response = {
                "message": f"Não foi possível excluir o Autor com o ID {author_id}"
            }

        return response

    @login_required
    def put(self, author_id: int):
        data = json.loads(request.data)

        try:
            author = Author.get_by_id(author_id)

            if author is not None:
                author.update(data)
                response = {
                    "message": "Dados atualizados com sucesso!",
                    "author": author.to_dict(),
                }

            else:
                response = {
                    "message": f"Não foi possível localizar os dados do Autor com o ID {author_id}"
                }

        except OperationalError:
            response = {
                "message": f"Erro ao atualizar dados do Autor com o ID {author_id}"
            }

        return response


class UserResource(Resource):
    def get(self, user_id: int):
        try:
            user = User.get_by_id(user_id)

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

    @login_required
    def put(self, user_id: int):
        status = 200
        data = json.loads(request.data)

        if not int(user_id) == current_user.id and current_user.is_admin:
            status = 401
            response = {
                "message": "Somente administradores estão autorizados a editar dados de outros usuarios."
            }

        else:
            try:
                data.pop("username", None)
                user = User.get_by_id(user_id)

                if user is not None:
                    user.update(data)
                    response = {
                        "message": "Dados atualizados com sucesso!",
                        "data": user.to_dict(),
                    }

                else:
                    response = {
                        "message": f"Não foi possível localizar os dados do Usuario com o ID {user_id}"
                    }

            except OperationalError:
                response = {
                    "message": f"Erro ao atualizar dados do Autor com o ID {user_id}"
                }

        return response, status

    @login_required
    def delete(self, user_id: int):
        status = 200
        if not current_user.is_admin:
            status = 401
            response = {
                "message": "Somente administradores estão autorizados a excluir usuarios."
            }

        else:
            try:
                user = User.get_by_id(user_id)
                if user is not None:
                    user_data = user.to_dict()
                    user.delete()
                    response = {
                        "message": "Usuario excluido com sucesso!",
                        "data": user_data,
                    }

                else:
                    response = {
                        "message": f"Não foi possível localizar o Usuario com o ID {user_id}"
                    }

            except OperationalError:
                response = {
                    "message": f"Não foi possível excluir o Usuario com o ID {user_id}"
                }

        return response, status


class UserAllResource(Resource):
    @login_required
    def get(self):
        if not current_user.is_admin:
            response = {
                "message": "Somente administradores estão autorizados a obter os dados dos usuarios."
            }

        else:
            try:
                data = [user.to_dict() for user in User.get_all()]

            except OperationalError:
                response = {"message": "Não foi possível obter a lista de usuarios"}

            else:
                response = data

        return response

    @login_required
    def post(self):
        data = json.loads(request.data)
        status = 200

        if not current_user.is_admin:
            status = 401
            response = {
                "message": "Somente administradores estão autorizados a cadastrar novos usuarios."
            }

        else:
            try:
                username = data["username"]
                password = data["password"]
                admin = True if data.get("admin", False) else False

                user = User.create(username, password, admin)

            except KeyError:
                response = {
                    "message": 'Os parametros ["username", "password"] são obrigatorios.'
                }

            except OperationalError:
                response = {
                    "message": "Não foi possível cadastrar o Usuario, verifique os parametros informados e tente novamente."
                }

            except IntegrityError:
                response = {"message": "Usuario já cadastrado no sistema!"}

            else:
                status = 201
                response = {
                    "message": "Usuario cadastrado com sucesso!",
                    "user": user.to_dict(),
                }

        return response, status
