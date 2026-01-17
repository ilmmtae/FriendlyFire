from fastapi import HTTPException

from src.schema.account import AgeResponse


class AccountService:
    @classmethod
    def calculate_age(cls, year: int) -> AgeResponse:
        if year < 0:
            # raise is used to throw an exception
            raise HTTPException(status_code=400, detail="Year cannot be negative")

        age =  2026 - year
        return AgeResponse(age=age)