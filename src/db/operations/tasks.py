from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from uuid import UUID
from fastapi import HTTPException, status

from src.db.models import Course
from src.db.models.task import Task
from src.schema.task import CreateTaskRequest, ShortTaskSchema


class TaskManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, request: CreateTaskRequest):
        course = await self.db.get(Course, request.course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found!"
            )

        data = request.model_dump()

        new_task = Task(**data)
        self.db.add(new_task)
        await self.db.commit()

        new_task = Task(**request.model_dump())
        self.db.add(new_task)
        await self.db.commit()
        await self.db.refresh(new_task)
        return new_task

    async def list_tasks(self):
        query = select(Task)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_tasks_by_course(self, course_id: UUID):
        query = select(Task).where(Task.course_id == course_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_task_by_id(self, task_id: UUID) -> Task:
        query = select(Task).where(Task.id == task_id)
        result = await self.db.execute(query)

        task = result.scalar_one_or_none()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return task

    async def delete_task_by_id(self, task_id: UUID) -> None:
        query = delete(Task).where(Task.id == task_id)
        await self.db.execute(query)
        await self.db.commit()

    async def update_task_by_id(self, task_id: UUID, request: ShortTaskSchema) -> Task:
        data = request.model_dump(exclude_unset=True)

        query = (
            update(Task)
            .where(Task.id == task_id)
            .values(**data)
            .returning(Task)
        )
        result = await self.db.execute(query)
        await self.db.commit()

        updated_task = result.scalar_one_or_none()
        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found")

        return updated_task