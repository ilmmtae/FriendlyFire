from enum import Enum


class AccountType(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
