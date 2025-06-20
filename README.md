# happycatAPI

Welcome to the **happycatAPI**, your source for internet-famous cat GIFs! Brighten your day or your app with the world’s most beloved feline memes.

<img src="https://media1.tenor.com/m/_hUq1BSUsiMAAAAC/cat-cute.gif" alt="Jumping happy cat" width="180" height="180">

## Technology Stack

- **Python** & **FastAPI** — Modern, async web framework
- **Uvicorn** — ASGI server for FastAPI
- **Pydantic** — Data validation and serialization
- **MongoDB** — Stores GIF metadata (title, tags, URL)
- **Pytest** — Automated testing (75+ test cases)

## Endpoints

### Public Endpoints

<details>
<summary><code>GET /</code> - Welcome endpoint</summary>

```
^>⩊<^ Welcome to the Happy Cat API ^>⩊<^

This API delivers GIFs of world-renowned cats — here to brighten your day.
Co-authored by Sujin Shin and Sungmin Cho.

Available endpoints:
GET /gifs           - Retrieve a list of all cat GIF memes
GET /gifs/{id}      - Retrieve details of a specific cat GIF meme
```

</details>

<details>
<summary><code>GET /gifs</code> - Retrieve a list of all cat GIF memes.</summary>

**Query Parameters:**  
`tag` (optional): Filter GIFs by tag.

```bash
$ curl -H "accept: application/json" https://happycatapi.onrender.com/gifs/
{
  "gifs": [
    {
      "id": "68533837cfec18989367b60b",
      "name": "happycat",
      "url": "https://tenor.com/bXAn9.gif",
      "tag": [
        "happy",
        "tabby",
        "happycat"
      ]
    },
    {
      "id": "685343594050c9b94faa4359",
      "name": "oiia",
      "url": "https://tenor.com/fFr2do9u7Kw.gif",
      "tag": [
        "oiia"
      ]
    },
    ...
  ]
}
```

</details>

<details>
<summary><code>GET /gifs/random</code> - Retrieve a random cat GIF meme.</summary>

```bash
$ curl -H "accept: application/json" https://happycatapi.onrender.com/gifs/random

{
  "id": "685382d38bf9e1317117dd96",
  "name": "huhcat",
  "url": "https://tenor.com/sqMU1WMDcgD.gif",
  "tag": ["huhcat"]
}
```

</details>

<details>
<summary><code>GET /gifs/{name}</code> - Retrieve details of a specific cat GIF meme by name.</summary>

```bash
$ curl -H "accept: application/json" https://happycatapi.onrender.com/gifs/chipichipi

{
  "id": "685382d48bf9e1317117dd97",
  "name": "chipichipi",
  "url": "https://tenor.com/dpqqxee0PFw.gif",
  "tag": ["chipichipi"]
}
```

</details>

---

### Restricted Endpoints (Require [Authentication](#Authentication))

<details>
<summary><code>POST /gifs</code> - Upload a new cat GIF meme.</summary>

**Body Example:**

```json
{
  "name": "happycat",
  "url": "https://tenor.com/bXAn9.gif",
  "tag": ["happy", "tabby"]
}
```

</details>

<details>
<summary><code>PUT /gifs/{id}</code> - Update a subset of a specific GIF meme's metadata.</summary>

**Body Example:**

```json
{
  "url": "https://tenor.com/newcat.gif",
  "tag": ["happy", "orange"]
}
```

</details>

<details>
<summary><code>DELETE /gifs/{id}</code> - Delete a specific GIF meme from the collection.</summary>
No body required.
</details>

## Authentication

Restricted endpoints require a valid admin token. Add in the header: `Authorization: Bearer <ADMIN_TOKEN>`

#### Example:

```bash
curl -X POST https://happycatapi.onrender.com/gifs \
  -H "accept: application/json" \
  -H "Authorization: Bearer <ADMIN_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name": "happycat", "url": "https://tenor.com/bXAn9.gif", "tag": ["happy"]}'
```

## Discord Bot Integration

The Happy Cat API powers a Discord bot that brings cat GIF joy directly to your server!

**Features (in development):**

- **/random** — Sends a random cat GIF in the activated channel.
- **/cotd** — Shares the Cat of Today (COTD).
- **/search [name]** — Fetches a specific cat GIF by name.

You can invite the beta version of the bot to your server using [this link](https://discord.com/oauth2/authorize?client_id=1380723035082063923&permissions=2048&integration_type=0&scope=bot).

See [**app/bot/**](/app/bot) for implementation details and updates.

## For Developers

### Getting Started

#### Clone the respository and install dependencies

```bash
$ git clone https://github.com/samcho02/happycatapi.git
$ cd happycatapi
$ pip install -r requirements.txt
```

#### Set up environment variables

Copy `.env.example` to `.env` and fill in your MongoDB URI and admin token.

#### Run the API server locally

`$ uvicorn app.main:app --reload`

- The API will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
- OpenAPI specification is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

#### Run the test suite

`$ pytest`

- 75+ automated tests ensure reliability and full coverage.

---

### Project Design

- **Modular Structure:**  
  The codebase is organized into clear modules for API routes, core logic, database access, schemas, and dependencies.
- **Async & Scalable:**  
  Built with FastAPI and async MongoDB drivers for high concurrency and performance.
- **Data Validation:**  
  All incoming and outgoing data is validated and serialized using Pydantic models.
- **Separation of Concerns:**  
  Public (GET) and restricted (POST/PUT/DELETE) endpoints are clearly separated and access-controlled.
- **Thoroughly Tested:**  
  All endpoints and edge cases are covered by automated pytest cases for confidence in every deployment.

### Contributing

Pull requests and issues are welcome!  
If you’d like to contribute, please fork the repo and submit a PR.

## Contact

For questions, feedback, or to request admin access, please contact  
[**szshn**](https://github.com/szshn) & [**samcho02**](https://github.com/samcho02)!
