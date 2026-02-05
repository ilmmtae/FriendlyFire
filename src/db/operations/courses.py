from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from src.db.models.courses import Course
from src.schema.courses import CreateCourseRequest, ShortCourseSchema


class CourseManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_course(self, request: CreateCourseRequest) -> Course:
        new_course = Course(
            **request.model_dump()
        )
        self.db.add(new_course)
        await self.db.commit()
        await self.db.refresh(new_course)
        return new_course

    async def list_courses(self):
        result = await self.db.execute(select(Course))
        return result.scalars().all()

    async def get_course_by_id(self, course_id: UUID):
        query = select(Course).where(Course.id == course_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def delete_course_by_id(self, course_id: UUID) -> None:
        query = delete(Course).where(Course.id == course_id)
        await self.db.execute(query)
        await self.db.commit()

    async def update_course_by_id(self, course_id: UUID, request: ShortCourseSchema) -> Course:
        query = (
            update(Course)
            .where(Course.id == course_id)
            .values(**request.model_dump(exclude_unset=True))
            .returning(Course)
        )
        result = await self.db.execute(query)
        await self.db.commit()

        updated_course = result.scalar_one_or_none()
        if not updated_course:
            raise HTTPException(status_code=404, detail="Course not found")

        return updated_course