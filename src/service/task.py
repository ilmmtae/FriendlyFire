from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Task
from src.db.operations.tasks import TaskManager
from src.schema.task import CreateTaskRequest, ShortTaskSchema


class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.manager = TaskManager

    async def create_task(self, request: CreateTaskRequest) -> Task:
        return await self.manager.create_task(request)

    async def get_tasks_by_course(self) -> List:
        return await self.manager.get_tasks_by_course()

    async def get_task_by_id(self) -> Task:
        return  await self.manager.get_task_by_id()

    async def list_tasks(self) -> List:
        return await self.manager.list_tasks()

    async def delete_task_by_id(self) -> None:
        return await self.manager.delete_task_by_id()

    async def update_task_by_id(self, request: ShortTaskSchema) -> Task:
        return await self.manager.update_task_by_id(request)



