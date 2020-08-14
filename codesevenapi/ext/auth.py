import json

from flask import jsonify, request
from flask_login import LoginManager, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from codesevenapi.ext.db.models import User

login_manager = LoginManager()


def init_app(app):
    login_manager.init_app(app)

    @app.route("/login/", methods=["POST"])
    def validate_user():
        data = json.loads(request.data)
        username = data.get("username", None)
        password = data.get("password", None)

        if username is None or password is None:
            response = {
                "message": 'Os parametros ["username", "password"] são obrigatorios.'
            }

        else:
            user = User.query.filter_by(username=username).first()

            if user is None:
                response = {"message": "Usuario não cadastrado!"}

            elif check_password_hash(user.password, password):
                login_user(user)

                response = {
                    "message": "Login realizado com sucesso!",
                    "user": user.to_dict(),
                }

            else:
                response = {
                    "message": "Credenciais invalidas, verifique seus dados e tente novamente."
                }

        return response

    @app.route("/logout/", methods=["GET"])
    def logout():
        logout_user()
        return {"message": "Sessão encerrada!"}


@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"message": "Você precisa estar logado para acessar este conteudo."})
