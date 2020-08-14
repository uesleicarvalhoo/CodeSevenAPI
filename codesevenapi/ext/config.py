def init_app(app):
    app.config["DEBUG_MODE"] = True
    app.config["SECRET_KEY"] = "\x15L\xcb\xa9d\xb4e1$X\xd5\xd7}z\xd8\x0c"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///codesevenapi.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_AS_ASCII"] = False
