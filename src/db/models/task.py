from uuid import uuid4

from sqlalchemy import Column, UUID, ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import relationship

from src.db.base import Base


class Task(Base):

    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"))
    task_title = Column(String)
    instructions = Column(String)
    max_score = Column(Integer, default=100)
    due_date = Column(DateTime)

    course = relationship("Course", back_populates="tasks")
