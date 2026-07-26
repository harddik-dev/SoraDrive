from fastapi import APIRouter

from ..controllers import auth_controller
from ..schemas.token import Token
from ..schemas.user import UserOut

router = APIRouter(prefix="/auth", tags=["auth"])

router.add_api_route(
    "/register", auth_controller.register, methods=["POST"], response_model=UserOut
)
router.add_api_route(
    "/login", auth_controller.login, methods=["POST"], response_model=Token
)
