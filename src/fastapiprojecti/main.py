import httpx
from contextlib import asynccontextmanager
from urllib.parse import urlencode

from fastapi import FastAPI, Request
from starlette.responses import RedirectResponse

from fastapiprojecti.api.v1.v1_router import router as v1_router
from fastapiprojecti.apps.auth.config import config
from fastapiprojecti.apps.auth.keycloak_client import KeycloakClient

@asynccontextmanager
async def lifespan(app: FastAPI):
    http_client = httpx.AsyncClient()
    app.state.keycloak_client = KeycloakClient(http_client)
    app.include_router(v1_router)

    yield

    await http_client.aclose()

app = FastAPI(lifespan=lifespan)

@app.get("/hello")
async def hello():
    return {"message": "Hello World"}
@app.get("/")
async def root(request: Request):
    access_token = request.cookies.get("access_token")
    if access_token:
        return RedirectResponse(url="/hello")

    params = {
        "client_id": config.KC_CLIENT_ID,
        "redirect_uri": config.REDIRECT_URI,
        "response_type": "code",
        "scope": "openid profile email",
    }

    keycloak_login_url = f"{config.KC_AUTH_URL}?{urlencode(params)}"

    return RedirectResponse(url=keycloak_login_url)


