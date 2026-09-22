from uuid import UUID

from pydantic import BaseModel


class UserSchema(BaseModel):
    sub: UUID
    email_verified: bool
    name: str
    preferred_username: str
    given_name: str
    family_name: str
    email: str

class RegisterSchema(BaseModel):
    username: str
    email: str
    password: str
