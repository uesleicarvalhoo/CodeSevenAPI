from dynaconf import FlaskDynaconf


def init_app(app):
    """Initialize Dynaconf to load configs"""
    FlaskDynaconf(app)
    app.config.load_extensions("EXTENSIONS")
