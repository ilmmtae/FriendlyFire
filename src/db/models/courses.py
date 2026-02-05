from datetime import datetime

from src.db.base import Base

from uuid import uuid4

from sqlalchemy import Column, UUID, String, DateTime, Boolean, func
from sqlalchemy.orm import relationship


class Course(Base):

    __tablename__ = "courses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, nullable=False)
    description = Column(String)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(), server_default=func.now())

    tasks = relationship(
        "Task",
        back_populates="course",
        cascade="all, delete-orphan",
    )


