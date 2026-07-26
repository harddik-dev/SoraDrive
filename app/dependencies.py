from fastapi import Depends
from sqlalchemy.orm import Session
from .core.database import get_db
from .repositories.user_repository import UserRepository
from .repositories.file_repository import FileRepository
from .services.auth_service import AuthService
from .services.file_service import FileService
from .services.s3_service import S3Service

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))

def get_file_service(db: Session = Depends(get_db)) -> FileService:
    return FileService(FileRepository(db), S3Service())