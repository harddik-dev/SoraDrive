from sqlalchemy.orm import Session
from ..models.file import File

class FileRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, owner_id: int, filename: str, file_key: str) -> File:
        file = File(owner_id=owner_id, filename=filename, file_key=file_key)
        self.db.add(file)
        self.db.commit()
        self.db.refresh(file)
        return file

    def get_owned_file(self, file_id: int, owner_id: int) -> File | None:
        return self.db.query(File).filter(
            File.id == file_id, File.owner_id == owner_id
        ).first()

    def delete(self, file: File):
        self.db.delete(file)
        self.db.commit()