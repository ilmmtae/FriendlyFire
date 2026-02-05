
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.operations.courses import CourseManager
from src.dependencies.database import RWSessionStub
from src.schema.courses import CreateCourseRequest, CourseResponse, ShortCourseSchema
from src.service.courses import CourseService

course_router = APIRouter(prefix="/course", tags=["course"])

@course_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new course",
    response_model=CourseResponse,
)
async def create_course(
    request: CreateCourseRequest,
    db: AsyncSession = Depends(RWSessionStub)
) -> CourseResponse:
    return await CourseService(db=db).create_course(request)


@course_router.get(
    "",
    summary="List all courses",
    response_model=List[CourseResponse],
)
async def list_courses(
    db: AsyncSession = Depends(RWSessionStub),
) -> List[CourseResponse]:
    return await CourseManager(db=db).list_courses()

@course_router.get(
    "/{course_id}",
    summary="Get course by ID",
    response_model=CourseResponse,
)
async def get_course_by_id(
    course_id: UUID,
    db: AsyncSession = Depends(RWSessionStub),
) -> CourseResponse:
    course = await CourseManager(db=db).get_course_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@course_router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: UUID,
    db: AsyncSession = Depends(RWSessionStub),
) -> None:
    return await CourseManager(db=db).delete_course_by_id(course_id)

@course_router.patch("/{course_id}", response_model=CourseResponse)
async def update_course(
    request: ShortCourseSchema,
    course_id: UUID,
    db: AsyncSession = Depends(RWSessionStub),
) -> CourseResponse:
    return await CourseManager(db=db).update_course_by_id(course_id=course_id, request=request)
