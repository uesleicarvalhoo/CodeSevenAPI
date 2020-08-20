import json


def test_app_is_created(app):
    assert app.name == "codesevenapi.app"


def test_config_is_load(config):
    assert config["DEBUG"] is False


def test_auth(client):
    response = client.get("/usuarios", follow_redirects=True)

    assert "Você precisa estar logado para acessar este conteudo" in response.get_data(
        as_text=True
    )


def test_invalid_login(client):
    response = client.post(
        "/login",
        data=json.dumps({"username": "usuario_nao_cadastrado", "password": "123"}),
        follow_redirects=True,
    )
    assert "Usuario não cadastrado" in response.get_data(as_text=True)


def test_login(app, client):
    with app.app_context():
        response = client.post(
            "/login",
            data=json.dumps({"username": "admin", "password": "admin"}),
            follow_redirects=True,
        )

        assert "Login realizado com sucesso!" in response.get_data(as_text=True)
        response = client.get("/logout", follow_redirects=True)
        assert "Sessão encerrada!" in response.get_data(as_text=True)
