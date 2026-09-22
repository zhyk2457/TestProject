from os import getenv


class Config:
    BASE_URL = getenv("APP_BASE_URL")

    KC_BASE_URL = getenv("KC_BASE_URL")
    KC_REALM_ID = getenv("KC_REALM_ID")
    KC_CLIENT_ID = getenv("KC_CLIENT_ID")
    KC_CLIENT_SECRET = getenv("KC_CLIENT_SECRET")

    REDIRECT_URI = getenv("REDIRECT_URI")

    KC_AUTH_URL = f"http://localhost:8080/realms/{KC_REALM_ID}/protocol/openid-connect/auth"
    KC_TOKEN_URL = f"{KC_BASE_URL}/realms/{KC_REALM_ID}/protocol/openid-connect/token"
    KC_LOGOUT_URL = getenv("KC_LOGOUT_URL")
    KC_USER_INFO_URL = f"{KC_BASE_URL}/realms/{KC_REALM_ID}/protocol/openid-connect/userinfo"


config = Config()