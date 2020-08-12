from flask import Flask
from codesevenapi.ext import config, cli, db, api

def create_app():
    app = Flask(__name__)
    config.init_app(app)
    db.init_app(app)
    cli.init_app(app)
    api.init_app(app)

    return app

# Criar os metodos Delete e Update para os Autores e Noticias
# Configurar o setup.py
# Utilizar o Dynaconf para as configurações(?)
# Criar a parte de autenticação
