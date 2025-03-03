import abc
from abc import abstractmethod
from typing import Any, Generic, Optional, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.abstraction import AbstractPokemonRepository
from repositories.relational_db import RelationalDBPokemonRepostory

T = TypeVar("T", bound=AbstractPokemonRepository)


class AbstractUnitOfWork(Generic[T], abc.ABC):
    pokemonRepo: AbstractPokemonRepository

    def __init__(self, pokemonRepo: T):
        self.pokemonRepo = pokemonRepo

    @abstractmethod
    async def __aenter__(self) -> 'AbstractUnitOfWork':
        raise NotImplemented
    
    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb):
        raise NotImplemented
    

class AsyncSQLAlchemyUnitOfWork(AbstractUnitOfWork[RelationalDBPokemonRepostory]):
    def __init__(self, session: AsyncSession, pokemonRepo: RelationalDBPokemonRepostory):
        super().__init__(pokemonRepo=pokemonRepo)
        self._session = session

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type: Optional[Type[BaseException]], exc: Optional[BaseException], tb: Any):
        try:
            if exc_type is None:
                await self._session.commit()
            else:
                await self._session.rollback()
        finally:
            await self._session.close()
            await self.remove()
    
    async def remove(self):
        from settings.db import AsyncScopedSession

        await AsyncScopedSession.remove()