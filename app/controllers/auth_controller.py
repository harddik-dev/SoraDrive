from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..dependencies import get_auth_service
from ..schemas.token import Token
from ..schemas.user import UserCreate, UserOut
from ..services.auth_service import AuthService


def register(
    payload: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserOut:
    user = auth_service.register(payload.email, payload.password)
    return UserOut.model_validate(user)


def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
) -> Token:
    # OAuth2PasswordRequestForm gives us `.username` / `.password` fields,
    # which is the standard shape FastAPI's swagger "Authorize" button expects.
    access_token = auth_service.authenticate(form_data.username, form_data.password)
    return Token(access_token=access_token)
