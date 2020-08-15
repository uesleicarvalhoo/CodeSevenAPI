from flask import Flask

from codesevenapi.ext import config


def create_app():
    """Factory for create app"""
    app = Flask(__name__)
    config.init_app(app)

    return app


# Testar o setup.py
# Documentar o código
# Pssar para o banco de dados para o MongoDB
# Criar os testes
