from src.db.base import Base

from uuid import uuid4

from sqlalchemy import Column, UUID, String, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Course(Base):

    __tablename__ = "courses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, nullable=False)
    description = Column(String)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime)

    tasks = relationship(
        "Task",
        back_populates="course",
        cascade="all, delete-orphan",
    )


class Task(Base):

    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"))
    task_title = Column(String, nullable=False)
    instructions = Column(String)
    max_score = Column(Integer, default=100)
    due_date = Column(DateTime)

    course = relationship("Course", back_populates="tasks")
