from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from ..core.database import Base

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    file_key = Column(String, nullable=False, unique=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    owner = relationship("User", back_populates="files")