from typing import List
from uuid import UUID

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.db.operations.tasks import TaskManager
from src.dependencies.database import RWSessionStub
from src.schema.task import TaskResponse, CreateTaskRequest, ShortTaskSchema

task_router = APIRouter(prefix="/task", tags=["task"])

@task_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    response_model=TaskResponse
    )
async def create_task(
    request: CreateTaskRequest,
    db: AsyncSession = Depends(RWSessionStub)
) -> TaskResponse:
    return await TaskManager(db=db).create_task(request)


@task_router.get(
    "",
    summary="List all tasks",
    response_model=List[TaskResponse],
)
async def list_tasks(
    db: AsyncSession = Depends(RWSessionStub),
) -> List[TaskResponse]:
    return await TaskManager(db=db).list_tasks()

@task_router.get(
    "/{task_id}",
    summary="Get tasks by ID",
    response_model=TaskResponse,
)
async def get_task_by_id(
    task_id: UUID,
    db: AsyncSession = Depends(RWSessionStub),
) -> TaskResponse:
    task = await TaskManager(db=db).get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@task_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    db: AsyncSession = Depends(RWSessionStub),
) -> None:
    return await TaskManager(db=db).delete_task_by_id(task_id)

@task_router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    request: ShortTaskSchema,
    task_id: UUID,
    db: AsyncSession = Depends(RWSessionStub),
) -> TaskResponse:
    return await TaskManager(db=db).update_task_by_id(task_id=task_id, request=request)


