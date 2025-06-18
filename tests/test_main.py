import pytest
from fastapi.testclient import TestClient
from app.main import app, intro_msg

client = TestClient(app)

class TestWelcome:
    def test_welcome_plain(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.text == intro_msg

    @pytest.mark.parametrize("accept", [
        "*/*",
        "text/plain"
    ])
    def test_welcome_accept_headers(self, accept):
        response = client.get("/", headers={"accept": accept})
        assert response.status_code == 200
        assert response.text == intro_msg

    @pytest.mark.parametrize("accept", [
        "image/png",
        "application/json"
    ])
    def test_welcome_invalid_accept(self, accept):
        response = client.get("/", headers={"accept": accept})
        assert response.status_code == 406

    @pytest.mark.parametrize("method", [
        "put", "post", "delete", "head", "patch"
    ])
    def test_welcome_illegal_methods(self, method):
        response = getattr(client, method)("/")
        assert response.status_code == 405