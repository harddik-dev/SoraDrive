from fastapi import HTTPException, status
from ..repositories.user_repository import UserRepository
from ..core.security import hash_password, verify_password, create_access_token

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, email: str, password: str):
        if self.user_repo.get_by_email(email):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already registered")
        return self.user_repo.create(email, hash_password(password))

    def authenticate(self, email: str, password: str) -> str:
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
        return create_access_token({"sub": str(user.id)})