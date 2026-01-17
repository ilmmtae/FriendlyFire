from fastapi import FastAPI

from src.api.account import account_router
from src.api.docs import docs_router

app = FastAPI()

app.include_router(account_router)
app.include_router(docs_router)

