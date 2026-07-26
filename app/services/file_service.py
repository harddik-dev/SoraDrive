from fastapi import HTTPException, status
from ..repositories.file_repository import FileRepository
from .s3_service import S3Service

class FileService:
    def __init__(self, file_repo: FileRepository, s3_service: S3Service):
        self.file_repo = file_repo
        self.s3 = s3_service

    def create_upload_url(self, user_id: int, filename: str, content_type: str):
        result = self.s3.generate_upload_url(user_id, filename, content_type)
        self.file_repo.create(user_id, filename, result["file_key"])
        return result

    def get_download_url(self, file_id: int, user_id: int) -> str:
        file = self.file_repo.get_owned_file(file_id, user_id)
        if not file:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "File not found")
        return self.s3.generate_download_url(file.file_key)

    def delete_file(self, file_id: int, user_id: int):
        file = self.file_repo.get_owned_file(file_id, user_id)
        if not file:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "File not found")
        self.s3.delete_file(file.file_key)
        self.file_repo.delete(file)