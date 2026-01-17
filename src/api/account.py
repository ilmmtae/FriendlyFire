from fastapi import APIRouter, Path

from src.schema.account import AgeResponse
from src.service.account import AccountService

account_router = APIRouter(
    prefix="/account", tags=["account"]
)

@account_router.get("/get_age/{year}")
def get_age(year: int = Path(..., description="The year of birth", le=2026)) -> AgeResponse:
    return AccountService.calculate_age(year)

# Write a post endpoint that takes a name and returns a greeting message (Enample "/account/greet/{name}" - "Hello, {name}!")
# 1. Pass name to the path
# 2. Pass name to the request body
# P.S - Both endpoints should be documented