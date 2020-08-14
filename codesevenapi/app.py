from flask import Flask

from codesevenapi.ext import api, auth, cli, config, db


def create_app():
    app = Flask(__name__)
    config.init_app(app)
    db.init_app(app)
    auth.init_app(app)
    cli.init_app(app)
    api.init_app(app)

    return app


# Utilizar o Dynaconf para as configurações(?)
# Testar o setup.py
# Documentar o código
# Pssar para o banco de dados para o MongoDB
# Resolver o problema do SQLAlchemy não validar a ForeignKey
