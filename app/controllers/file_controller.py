from fastapi import Depends
from ..schemas.file import UploadRequest
from ..services.file_service import FileService
from ..dependencies import get_file_service
from ..core.security import get_current_user

class FileController:
    def __init__(self, service: FileService = Depends(get_file_service)):
        self.service = service

    def request_upload_url(self, payload: UploadRequest, user_id: int = Depends(get_current_user)):
        return self.service.create_upload_url(user_id, payload.filename, payload.content_type)

    def get_download_url(self, file_id: int, user_id: int = Depends(get_current_user)):
        return {"download_url": self.service.get_download_url(file_id, user_id)}

    def delete_file(self, file_id: int, user_id: int = Depends(get_current_user)):
        self.service.delete_file(file_id, user_id)
        return {"status": "deleted"}