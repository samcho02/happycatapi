import pytest
from fastapi.testclient import TestClient
from app.main import app, welcome_msg
from app.schemas.gifs import GIFcollection
from app.db.gifs_test_db import gifs_test_db

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

class TestWelcome:
    """Tests for the root welcome endpoint."""

    @pytest.mark.parametrize("accept", [None, "*/*", "text/plain"])
    def test_welcome_accepts_plain(self, client, accept):
        headers = {"accept": accept} if accept else {}
        response = client.get("/", headers=headers)
        assert response.status_code == 200
        assert response.text == welcome_msg

    @pytest.mark.parametrize("method", ["put", "post", "delete", "head", "patch"])
    def test_welcome_illegal_methods(self, client, method):
        response = getattr(client, method)("/")
        assert response.status_code == 405

    @pytest.mark.parametrize("accept", ["image/png", "application/json"])
    def test_welcome_rejects_invalid_accept(self, client, accept):
        response = client.get("/", headers={"accept": accept})
        assert response.status_code == 406

class TestGetAll:
    """Tests for the /gifs/ endpoint."""

    @pytest.mark.parametrize("accept", [None, "*/*", "application/json"])
    def test_getall_accepts_json(self, client, accept):
        headers = {"accept": accept} if accept else {}
        response = client.get("/gifs/", headers=headers)
        assert response.status_code == 200
        assert isinstance(GIFcollection(**(response.json())), GIFcollection)

    @pytest.mark.parametrize("method", ["put", "post", "delete", "head", "patch"])
    def test_getall_illegal_methods(self, client, method):
        response = getattr(client, method)("/gifs/")
        assert response.status_code == 405

    @pytest.mark.parametrize("accept", ["text/plain", "image/png"])
    def test_getall_rejects_invalid_accept(self, client, accept):
        response = client.get("/gifs/", headers={"accept": accept})
        assert response.status_code == 406

class TestGetRandom:
    """Tests for the /gifs/random endpoint."""

    def test_random_returns_gif(self, client):
        response = client.get("/gifs/random")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert all(key in response.json() for key in {"id", "name", "url", "tag"})

    def test_random_returns_randomness(self, client):
        responses = [client.get("/gifs/random").json()["id"] for _ in range(3)]
        assert len(set(responses)) > 1  # At least two different GIFs

    @pytest.mark.parametrize("accept", [None, "*/*", "application/json"])
    def test_random_accepts_json(self, client, accept):
        headers = {"accept": accept} if accept else {}
        response = client.get("/gifs/random", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.parametrize("method", ["put", "post", "delete", "head", "patch"])
    def test_random_illegal_methods(self, client, method):
        response = getattr(client, method)("/gifs/random")
        assert response.status_code == 405

    @pytest.mark.parametrize("accept", ["text/plain", "image/png"])
    def test_random_rejects_invalid_accept(self, client, accept):
        response = client.get("/gifs/random", headers={"accept": accept})
        assert response.status_code == 406

class TestGetByName:
    """Tests for the /gifs/{name} endpoint."""

    oiia_response = {
        "id": "7",
        "name": "oiia",
        "url": "https://tenor.com/fFr2do9u7Kw.gif",
        "tag": ["oiia"]
    }

    @pytest.mark.parametrize("accept", [None, "*/*", "application/json"])
    def test_get_by_name_accepts_json(self, client, accept):
        headers = {"accept": accept} if accept else {}
        response = client.get("/gifs/oiia", headers=headers)
        assert response.status_code == 200
        assert response.json() == self.oiia_response
    
    def test_get_by_name_nonexisting(self, client):
        response = client.get("/gifs/uiia")
        assert response.status_code == 404
        assert response.json() == {"detail": 'GIF with name "uiia" not found'}

    @pytest.mark.parametrize("method", ["put", "post", "delete", "head", "patch"])
    def test_get_by_name_illegal_methods(self, client, method):
        response = getattr(client, method)("/gifs/oiia")
        assert response.status_code == 405

    @pytest.mark.parametrize("accept", ["text/plain", "image/png"])
    def test_get_by_name_rejects_invalid_accept(self, client, accept):
        response = client.get("/gifs/oiia", headers={"accept": accept})
        assert response.status_code == 406