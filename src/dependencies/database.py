from sqlalchemy.orm import Session

from src.dependencies.stub import Stub


async def get_db() -> Session:
    raise NotImplementedError("Use async DB connection instead")


class RWDatabaseStub(Stub):
    pass


class RWSessionStub(Stub):
    pass
