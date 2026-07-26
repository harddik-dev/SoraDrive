from pydantic import BaseModel

class UploadRequest(BaseModel):
    filename: str
    content_type: str

class FileOut(BaseModel):
    id: int
    filename: str
    class Config:
        from_attributes = True