import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from app.main import app, welcome_msg
from app.schemas.gifs import GIFcollection
from app.db.gifs_test_db import gifs_test_db

pytestmark = pytest.mark.anyio

@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

class TestWelcome:
    """Tests for the root welcome endpoint."""

    @pytest.mark.parametrize("accept", [None, "*/*", "text/plain"])
    async def test_welcome_accepts_plain(self, async_client, accept):
        headers = {"accept": accept} if accept else {}
        response = await async_client.get("/", headers=headers)
        assert response.status_code == 200
        assert response.text == welcome_msg

    @pytest.mark.parametrize("method", ["put", "post", "delete", "head", "patch"])
    async def test_welcome_illegal_methods(self, async_client, method):
        response = await getattr(async_client, method)("/")
        assert response.status_code == 405

    @pytest.mark.parametrize("accept", ["image/png", "application/json"])
    async def test_welcome_rejects_invalid_accept(self, async_client, accept):
        response = await async_client.get("/", headers={"accept": accept})
        assert response.status_code == 406

class TestGetAll:
    """Tests for the /gifs/ endpoint."""

    @pytest.mark.parametrize("accept", [None, "*/*", "application/json"])
    async def test_getall_accepts_json(self, async_client, accept):
        headers = {"accept": accept} if accept else {}
        response = await async_client.get("/gifs/", headers=headers)
        assert response.status_code == 200
        assert isinstance(GIFcollection(**(response.json())), GIFcollection)

    @pytest.mark.parametrize("method", ["put", "delete", "head", "patch"])
    async def test_getall_illegal_methods(self, async_client, method):
        response = await getattr(async_client, method)("/gifs/")
        assert response.status_code == 405

    @pytest.mark.parametrize("accept", ["text/plain", "image/png"])
    async def test_getall_rejects_invalid_accept(self, async_client, accept):
        response = await async_client.get("/gifs/", headers={"accept": accept})
        assert response.status_code == 406
        
class TestGetRandom:
    """Tests for the /gifs/random endpoint."""

    async def test_random_returns_gif(self, async_client):
        response = await async_client.get("/gifs/random")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert all(key in response.json() for key in {"id", "name", "url", "tag"})

    async def test_random_returns_randomness(self, async_client):
        responses = [(await async_client.get("/gifs/random")).json()["id"] for _ in range(3)]
        assert len(set(responses)) > 1  # At least two different GIFs

    @pytest.mark.parametrize("accept", [None, "*/*", "application/json"])
    async def test_random_accepts_json(self, async_client, accept):
        headers = {"accept": accept} if accept else {}
        response = await async_client.get("/gifs/random", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.parametrize("method", ["put", "post", "delete", "head", "patch"])
    async def test_random_illegal_methods(self, async_client, method):
        response = await getattr(async_client, method)("/gifs/random")
        assert response.status_code == 405

    @pytest.mark.parametrize("accept", ["text/plain", "image/png"])
    async def test_random_rejects_invalid_accept(self, async_client, accept):
        response = await async_client.get("/gifs/random", headers={"accept": accept})
        assert response.status_code == 406

class TestGetByName:
    """Tests for the /gifs/{name} endpoint."""

    oiia_response = {
        "id": "685343594050c9b94faa4359",
        "name": "oiia",
        "url": "https://tenor.com/fFr2do9u7Kw.gif",
        "tag": ["oiia"]
    }

    @pytest.mark.parametrize("accept", [None, "*/*", "application/json"])
    async def test_get_by_name_accepts_json(self, async_client, accept):
        headers = {"accept": accept} if accept else {}
        response = await async_client.get("/gifs/oiia", headers=headers)
        assert response.status_code == 200
        assert response.json() == self.oiia_response
        
    async def test_get_by_name_nonexisting(self, async_client):
        response = await async_client.get("/gifs/uiia")
        assert response.status_code == 404
        assert response.json() == {"detail": 'GIF with name "uiia" not found'}

    @pytest.mark.parametrize("method", ["put", "post", "delete", "head", "patch"])
    async def test_get_by_name_illegal_methods(self, async_client, method):
        response = await getattr(async_client, method)("/gifs/oiia")
        assert response.status_code == 405
        
    @pytest.mark.parametrize("accept", ["text/plain", "image/png"])
    async def test_get_by_name_rejects_invalid_accept(self, async_client, accept):
        response = await async_client.get("/gifs/oiia", headers={"accept": accept})
        assert response.status_code == 406

class TestGetByTag:
    """Tests for the /gifs/ endpoint with tag parameter"""

    @pytest.mark.parametrize("accept", [None, "*/*", "application/json"])
    async def test_get_by_tag_accepts_json(self, async_client, accept):
        headers = {"accept": accept} if accept else {}
        response = await async_client.get("/gifs/?tag=happycat", headers=headers)
        assert response.status_code == 200
        assert isinstance(GIFcollection(**(response.json())), GIFcollection)
    
    async def test_get_by_tag_nonexisting(self, async_client):
        response = await async_client.get("/gifs/?tag=uiia")
        assert response.status_code == 404
        assert response.json() == {"detail": 'GIF with tag "uiia" not found'}

    @pytest.mark.parametrize("method", ["put", "post", "delete", "head", "patch"])
    async def test_get_by_tag_illegal_methods(self, async_client, method):
        response = await getattr(async_client, method)("/gifs/?tag=happycat")
        assert response.status_code == 405

    @pytest.mark.parametrize("accept", ["text/plain", "image/png"])
    async def test_get_by_tag_rejects_invalid_accept(self, async_client, accept):
        response = await async_client.get("/gifs/?tag=happycat", headers={"accept": accept})
        assert response.status_code == 406