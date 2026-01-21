from abc import ABC, abstractmethod
from typing import Any


class Stub:
    """
    Stub class for FastAPI DI system,
    which allows to use `Depends` without any real dependencies in the code.
    """


class BaseInject(ABC):
    """
    A base abstract class for dependency injection.

    The `BaseInject` class should be inherited by other classes that provide specific
     implementations of dependency injection.
    The inherited classes should implement the `__call__` method with the desired logic
     for the injection.

    Notes:
    - This class is an abstract base class and should not be instantiated directly.
    - The `__call__` method should be implemented by inheriting classes.
    - The return type of the `__call__` method should be specified in the implementation
     as specified by the `-> Any` type hint.
    """

    @abstractmethod
    async def __call__(self) -> Any:
        pass


class InjectStatic(BaseInject):
    """
    Class for injecting static values into an async function.
    """

    def __init__(self, target: Any) -> None:
        self.target = target

    async def __call__(self) -> Any:
        return self.target


class InjectContextManager(BaseInject):
    """
    Class for injecting value from context manager into an async function.
    """

    def __init__(self, target: Any) -> None:
        self.target = target

    async def __call__(self) -> Any:
        async with self.target() as value:
            yield value
