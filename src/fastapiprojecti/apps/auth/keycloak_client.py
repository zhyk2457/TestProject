import httpx
from fastapi import HTTPException

from fastapiprojecti.apps.auth.config import config

class KeycloakClient:
    def __init__(self, client: httpx.AsyncClient | None = None):
        self.client = client or httpx.AsyncClient()

    async def get_tokens(self, code: str) -> dict:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": config.REDIRECT_URI,
            "client_id": config.KC_CLIENT_ID,
            "client_secret": config.KC_CLIENT_SECRET,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            response = await self.client.post(
                config.KC_TOKEN_URL, data=data, headers=headers
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=401, detail=f"Token request failed: {response.text}"
                )
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500, detail=f"Token exchange failed: {str(e)}"
            )

    async def get_user_info(self, token: str) -> dict:
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = await self.client.get(config.KC_USER_INFO_URL, headers=headers)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=401, detail=f"Invalid access token: {response.text}"
                )
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500, detail=f"Keycloak request error: {str(e)}"
            )