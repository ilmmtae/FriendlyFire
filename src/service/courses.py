from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.courses import Course
from src.db.operations.courses import CourseManager
from src.schema.courses import CreateCourseRequest, ShortCourseSchema


class CourseService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.manager = CourseManager(db=db)

    async def create_course(self, request: CreateCourseRequest) -> Course:
        return await self.manager.create_course(request)

    async def list_courses(self) -> List:
        return await self.manager.list_courses()

    async def get_course_by_id(self) -> List:
        return await self.manager.get_course_by_id()

    async def delete_course_by_id(self) -> None:
        return await self.manager.delete_course_by_id()

    async def update_course_by_id(self, request: ShortCourseSchema) -> Course:
        return await self.manager.update_course_by_id(request)