def test_app_is_created(app):
    assert app.name == "codesevenapi.app"


def teste_config_is_load(config):
    assert config["DEBUG"] is False
