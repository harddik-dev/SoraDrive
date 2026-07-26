from fastapi import APIRouter, Depends
from ..controllers.file_controller import FileController

router = APIRouter(prefix="/files", tags=["files"])

@router.post("/upload-url")
def upload_url(controller: FileController = Depends()):
    return controller.request_upload_url

@router.get("/{file_id}/download-url")
def download_url(controller: FileController = Depends()):
    return controller.get_download_url

@router.delete("/{file_id}")
def delete(controller: FileController = Depends()):
    return controller.delete_file