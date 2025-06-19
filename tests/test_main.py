import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient
from app.main import app, welcome_msg
from app.schemas.gifs import GIFcollection

import os
from dotenv import load_dotenv

pytestmark = pytest.mark.anyio

load_dotenv()
ADMIN_TOKEN = os.environ["ADMIN_TOKEN"]

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
        assert response.status_code == status.HTTP_200_OK
        assert response.text == welcome_msg

    @pytest.mark.parametrize("method", ["put", "post", "delete", "head", "patch"])
    async def test_welcome_illegal_methods(self, async_client, method):
        response = await getattr(async_client, method)("/")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    @pytest.mark.parametrize("accept", ["image/png", "application/json"])
    async def test_welcome_rejects_invalid_accept(self, async_client, accept):
        response = await async_client.get("/", headers={"accept": accept})
        assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE

class TestGetAll:
    """Tests for the /gifs/ endpoint."""

    @pytest.mark.parametrize("accept", [None, "*/*", "application/json"])
    async def test_getall_accepts_json(self, async_client, accept):
        headers = {"accept": accept} if accept else {}
        response = await async_client.get("/gifs/", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(GIFcollection(**(response.json())), GIFcollection)

    @pytest.mark.parametrize("method", ["put", "delete", "head", "patch"])
    async def test_getall_illegal_methods(self, async_client, method):
        response = await getattr(async_client, method)("/gifs/")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    @pytest.mark.parametrize("accept", ["text/plain", "image/png"])
    async def test_getall_rejects_invalid_accept(self, async_client, accept):
        response = await async_client.get("/gifs/", headers={"accept": accept})
        assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
        
class TestGetRandom:
    """Tests for the /gifs/random endpoint."""

    async def test_random_returns_gif(self, async_client):
        response = await async_client.get("/gifs/random")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), dict)
        assert all(key in response.json() for key in {"id", "name", "url", "tag"})

    async def test_random_returns_randomness(self, async_client):
        responses = [(await async_client.get("/gifs/random")).json()["id"] for _ in range(3)]
        assert len(set(responses)) > 1  # At least two different GIFs

    @pytest.mark.parametrize("accept", [None, "*/*", "application/json"])
    async def test_random_accepts_json(self, async_client, accept):
        headers = {"accept": accept} if accept else {}
        response = await async_client.get("/gifs/random", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), dict)
        
    @pytest.mark.parametrize("method", ["put", "delete"])
    async def test_random_rejects_override(self, async_client, method):
        response = await getattr(async_client, method)("/gifs/random")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("method", ["post", "head", "patch"])
    async def test_random_illegal_methods(self, async_client, method):
        response = await getattr(async_client, method)("/gifs/random")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    @pytest.mark.parametrize("accept", ["text/plain", "image/png"])
    async def test_random_rejects_invalid_accept(self, async_client, accept):
        response = await async_client.get("/gifs/random", headers={"accept": accept})
        assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE

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
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == self.oiia_response
    
    @pytest.mark.parametrize("method", ["put", "delete"])
    async def test_get_by_name_rejects_override(self, async_client, method):
        response = await getattr(async_client, method)("/gifs/oiia")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    async def test_get_by_name_nonexisting(self, async_client):
        response = await async_client.get("/gifs/uiia")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": 'GIF with name "uiia" not found'}

    @pytest.mark.parametrize("method", ["post", "head", "patch"])
    async def test_get_by_name_illegal_methods(self, async_client, method):
        response = await getattr(async_client, method)("/gifs/oiia")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        
    @pytest.mark.parametrize("accept", ["text/plain", "image/png"])
    async def test_get_by_name_rejects_invalid_accept(self, async_client, accept):
        response = await async_client.get("/gifs/oiia", headers={"accept": accept})
        assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE

class TestGetByTag:
    """Tests for the /gifs/ endpoint with tag parameter"""

    @pytest.mark.parametrize("accept", [None, "*/*", "application/json"])
    async def test_get_by_tag_accepts_json(self, async_client, accept):
        headers = {"accept": accept} if accept else {}
        response = await async_client.get("/gifs/?tag=happycat", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(GIFcollection(**(response.json())), GIFcollection)

    async def test_get_by_tag_rejects_override(self, async_client):
        response = await async_client.post("/gifs/?tag=happycat")
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    async def test_get_by_tag_nonexisting(self, async_client):
        response = await async_client.get("/gifs/?tag=uiia")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": 'GIF with tag "uiia" not found'}

    @pytest.mark.parametrize("method", ["put", "delete", "head", "patch"])
    async def test_get_by_tag_illegal_methods(self, async_client, method):
        response = await getattr(async_client, method)("/gifs/?tag=happycat")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    @pytest.mark.parametrize("accept", ["text/plain", "image/png"])
    async def test_get_by_tag_rejects_invalid_accept(self, async_client, accept):
        response = await async_client.get("/gifs/?tag=happycat", headers={"accept": accept})
        assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE

@pytest.fixture(scope="module")
async def created_gif_id(async_client):
    payload = {"name": "testcat", "url": "https://tenor.com/bdKzXnPAcGB.gif", "tag": ["test"]}
    headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
    response = await async_client.post("/gifs/", json=payload, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "testcat"
    assert response.json()["tag"] == ["test"]
    
    return response.json()["id"]   # Store for other tests

class TestAdd:
    async def test_add_accepts_initial(self, created_gif_id):
        # Make sure name=testcat doesn't exist in DB
        assert created_gif_id is not None
    
    async def test_add_rejects_no_authentication(self, async_client):
        payload = {"name": "test", "url": "https://tenor.com/h6lnHdUVixW.gif", "tag": ["test"]}
        response = await async_client.post("/gifs/", json=payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN  # While this really should be 401, it is a known Fast API bug under fix.
    
    async def test_add_rejects_no_authorization(self, async_client):
        payload = {"name": "test", "url": "https://tenor.com/h6lnHdUVixW.gif", "tag": ["test"]}
        headers = {"Authorization": f"Bearer clearlynotavalidtoken"}
        response = await async_client.post("/gifs/", json=payload, headers=headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    @pytest.mark.parametrize("accept", ["text/plain", "image/png"])
    async def test_add_rejects_invalid_accept(self, async_client, accept):
        payload = {"name": "test", "url": "https://tenor.com/h6lnHdUVixW.gif", "tag": ["test"]}
        headers = {"Authorization": f"Bearer {ADMIN_TOKEN}", "accept": accept}
        response = await async_client.post("/gifs/", json=payload, headers=headers)
        assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
    
    async def test_add_rejects_duplicate_name(self, async_client):
        payload = {"name": "testcat", "url": "https://tenor.com/bdKzXnPAcGB.gif", "tag": ["test"]}
        headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
        response = await async_client.post("/gifs/", json=payload, headers=headers)
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json()["detail"] == "Conflict: A GIF named testcat already exists."
    
    async def test_add_rejects_duplicate_url(self, async_client, created_gif_id):
        payload = {"name": "test", "url": "https://tenor.com/bdKzXnPAcGB.gif", "tag": ["test"]}
        headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
        response = await async_client.post("/gifs/", json=payload, headers=headers)
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json()["detail"] == f"Conflict: URL is tied to another GIF (id={created_gif_id})."
    
    async def test_add_rejects_missing_tag(self, async_client):
        payload = {"name": "test", "url": "https://tenor.com/h6lnHdUVixW.gif"}
        headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
        response = await async_client.post("/gifs/", json=payload, headers=headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
    async def test_add_rejects_invalid_url(self, async_client):
        payload = {"name": "test", "url": "", "tag": []}
        headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
        response = await async_client.post("/gifs/", json=payload, headers=headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    """
    Fail: Add a GIF without authentication
    - Omit the token or use an invalid token.
    - Assert 403 Forbidden or 401 Unauthorized.
    
    Fail: Add a GIF with duplicate name or URL
    - Add a GIF with a name or URL that already exists.
    - Assert 409 Conflict or your chosen error code/message.
    
    Fail: Add a GIF with missing required fields
    - Omit required fields (e.g., name, url).
    - Assert 422 Unprocessable Entity.
    
    Fail: Add a GIF with invalid URL format
    - Use an invalid URL in the payload.
    - Assert 422 Unprocessable Entity.
    """

class TestUpdate:
    """
    Success: Update an existing GIF (with valid token)
    - Send a valid update payload and a valid token for an existing GIF ID.
    - Assert 200 OK and response reflects the update.

    Fail: Update a non-existing GIF
    - Use a valid token and a non-existent ID.
    - Assert 404 Not Found.

    Fail: Update with invalid or missing fields
    - Send an invalid payload (e.g., missing required fields).
    - Assert 422 Unprocessable Entity.

    Fail: Update with duplicate name or URL
    - Try to update a GIF to a name or URL that already exists for another GIF.
    - Assert 409 Conflict or your chosen error code/message.

    Fail: Update without authentication
    - Omit the token or use an invalid token.
    - Assert 403 Forbidden or 401 Unauthorized.

    Fail: Update with invalid ID format
    - Use an invalid ID (not a valid ObjectId).
    - Assert 422 Unprocessable Entity or 400 Bad Request.
    """
    
class TestDelete:
    """
    Success: Delete an existing GIF (with valid token)
    - Send a valid delete payload and a valid token for an existing GIF ID.
    - Assert 204 No Content.
        
    Fail: Delete a non-existing GIF
    - Use a valid token and a non-existent ID.
    - Assert 404 Not Found.

    Fail: Update without authentication
    - Omit the token or use an invalid token.
    - Assert 403 Forbidden or 401 Unauthorized.
    
    Fail: Update with invalid ID format
    - Use an invalid ID (not a valid ObjectId).
    - Assert 422 Unprocessable Entity or 400 Bad Request.
    """