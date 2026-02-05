from fastapi import FastAPI

from src.api.course import course_router
from src.api.task import task_router
from src.config.db import setup_database
from src.api.account import account_router
from src.api.docs import docs_router


from src.db.models import account, courses

app = FastAPI()
setup_database(app)
app.include_router(task_router)
app.include_router(account_router)
app.include_router(course_router)
app.include_router(docs_router, include_in_schema=False)
