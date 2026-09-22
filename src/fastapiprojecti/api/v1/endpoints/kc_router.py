from fastapi import APIRouter, HTTPException, Depends, Request
from fastapiprojecti.apps.auth.config import config
from urllib.parse import urlencode
from fastapi.responses import RedirectResponse
from fastapiprojecti.apps.auth.auth_dep import get_keycloak_client
from fastapiprojecti.apps.auth.keycloak_client import KeycloakClient

router = APIRouter(
    prefix="/keycloak-auth",
    tags=["keycloak-auth"],
)

@router.get("/login/callback", include_in_schema=False)
async def login_callback(
    code: str | None = None,
    error: str | None = None,
    error_description: str | None = None,
    keycloak: KeycloakClient = Depends(get_keycloak_client),
) -> RedirectResponse:
    if error:
        raise HTTPException(status_code=400, detail=f"Keycloak authorization error: {error_description or error}")

    if not code:
        raise HTTPException(status_code=401, detail="Authorization code is required")

    try:
        # Получение токенов от Keycloak
        token_data = await keycloak.get_tokens(code)
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        id_token = token_data.get("id_token")

        if not access_token:
            raise HTTPException(status_code=401, detail="Токен доступа не найден")
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token не найден")
        if not id_token:
            raise HTTPException(status_code=401, detail="ID token не найден")


        # Установка cookie с токенами и редирект
        response = RedirectResponse(url="/hello")
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            path="/",
            max_age=token_data.get("expires_in", 3600),
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            path="/",
            max_age=token_data.get("refresh_expires_in", 2592000),
        )
        response.set_cookie(
            key="id_token",
            value=id_token,
            httponly=True,
            secure=False,
            samesite="lax",
            path="/",
            max_age=token_data.get("expires_in", 3600),
        )
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error during authentication")


@router.get("/logout", include_in_schema=False)
async def logout(request: Request):
    id_token = request.cookies.get("id_token")
    params = {
        "client_id": config.KC_CLIENT_ID,
        "post_logout_redirect_uri": config.BASE_URL,
    }
    if id_token:
        params["id_token_hint"] = id_token

    keycloak_logout_url = f"{config.KC_LOGOUT_URL}?{urlencode(params)}"
    response = RedirectResponse(url=keycloak_logout_url)
    for cookie_name in ["access_token", "refresh_token", "id_token"]:
        response.delete_cookie(
            key=cookie_name,
            httponly=True,
            secure=False,
            samesite="lax",
            path="/",
        )
    return response
