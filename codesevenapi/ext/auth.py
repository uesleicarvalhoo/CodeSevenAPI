import json

from flask import jsonify, request
from flask_login import LoginManager, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from codesevenapi.ext.db.models import User

login_manager = LoginManager()


def init_app(app):
    """Init the Flask-login extension"""
    login_manager.init_app(app)

    @app.route("/login", methods=["POST", "GET"])
    def validate_user():
        """Function used by Flask-login to validate the user"""

        if request.method == "GET":
            response = {
                "message": "Para realizar o login na página envie um POST contendo o username e password no body da requisição."  # noqa
            }

        elif request.method == "POST":
            data = json.loads(request.get_data(as_text=True))
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

        return jsonify(response)

    @app.route("/logout", methods=["GET"])
    @login_required
    def logout():
        """End the User session"""
        logout_user()
        return jsonify({"message": "Sessão encerrada!"})


@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"message": "Você precisa estar logado para acessar este conteudo."})
