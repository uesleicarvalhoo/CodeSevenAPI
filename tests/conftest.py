import pytest

from codesevenapi.app import create_app


@pytest.fixture(scope="module")
def app():
    flask_app = create_app()

    return create_app()
