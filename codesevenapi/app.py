from flask import Flask

from codesevenapi.ext import config


def create_app():
    """Factory for create app,"""
    app = Flask(__name__)
    config.init_app(app)

    return app
