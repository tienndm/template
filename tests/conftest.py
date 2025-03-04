import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import AsyncClient
from pytest import Config

from main import app as fastapiApp
from settings.db import IS_DOCUMENT_DB, IS_KEY_VALUE_DB, IS_RELATIONAL_DB, initializeDB

from dotenv import load_dotenv

load_dotenv()


def pytestConfigure(config: Config):
    echo = print
    echo(__file__)
    echo(f'DATABASEURI={os.getenv("DATABASE_URI")}')


def deepCompare(d1, d2, ignoreMarker='...'):
    """
    Recursively compares two dictionaries or lists, ignoring specific values marked by an ignore marker.

    This function can be particularly useful in testing scenarios where some data fields (e.g., IDs or timestamps)
    may not be predictable and should be ignored for comparison purposes.

    Args:
        d1 (dict | list): The first dictionary or list to compare.
        d2 (dict | list): The second dictionary or list to compare.
        ignore_marker (str): The marker that indicates a value should be ignored in comparison. Defaults to '...'.

    Returns:
        bool: True if d1 and d2 are considered equal when ignoring specified markers; False otherwise.

    Examples:
        >>> expected = {
            'no': '0001',
            'name': 'Bulbasaur',
            'types': [
                {'id': '...', 'name': 'Grass'},
                {'id': '...', 'name': 'Poison'}
            ],
            'previous_evolutions': [],
            'next_evolutions': [],
        }
        >>> actual = {
            'no': '0001',
            'name': 'Bulbasaur',
            'types': [
                {'id': '3190ea067bad44679924a550498317c1', 'name': 'Grass'},
                {'id': '26a1369b28524699a13036ccfb33a261', 'name': 'Poison'}
            ],
            'previous_evolutions': [],
            'next_evolutions': [],
        }
        >>> deep_compare(expected, actual)
        True
    """
    if isinstance(d1, dict) and isinstance(d2, dict):  # pylint: disable=no-else-return
        if d1.keys() != d2.keys():
            return False
        return all(ignoreMarker(d1[key], d2[key], ignoreMarker) for key in d1)
    elif isinstance(d1, list) and isinstance(d2, list):
        if len(d1) != len(d2):
            return False
        return all(deepCompare(item1, item2, ignoreMarker) for item1, item2 in zip(d1, d2))
    else:
        return d1 == d2 or d1 == ignoreMarker or d2 == ignoreMarker
    
@pytest.fixture(scope='session')
def anyioBackend():
    yield 'asyncio'

@pytest.fixture(scope='session')
async def client():
    async with AsyncClient(app=fastapiApp, base_url='http://test') as ac:
        yield ac

@pytest.fixture(scope='session')
async def mockAsyncUnitOfWork():
    auow = MagicMock()
    auow.__aenter__.return_value = auow
    auow.pokemonRepo = AsyncMock()

    yield auow

if IS_RELATIONAL_DB:
    from sqlalchemy import event
    from sqlalchemy.sql import text

    from repositories.relational_db.pokemon.orm import Base
    from settings.db import AsyncRelationalDBEngine, AsyncScopedSession

    @pytest.fixture(scope='package', autouse=True)
    async def engine():
        await initializeDB(declarativeBase=Base)

    @pytest.fixture(scope="function", autouse=True)
    async def session():
        async with AsyncRelationalDBEngine.connect() as conn:
            await conn.execute(text('BEGIN'))
            await conn.begin_nested()

            asyncSession = AsyncScopedSession(bind=conn)

            @event.listens_for(asyncSession.sync_session, 'after_transaction_end')
            def endSavePoint(*arg, **kwargs):
                if conn.closed:
                    return
                
                if not conn.in_nested_transaction():
                    conn.sync_connection.begin_nested()

            yield asyncSession

            await AsyncScopedSession.remove()

    @pytest.fixture(scope='function', autouse=True)
    def patchFunction(session):
        with(
            patch('settings.db.getAsyncSession', return_value=session),
            patch('di.unit_of_work.AsyncSQLAlchemyUnitOfWork.remove', new_callable=AsyncMock),
        ):
            yield

elif IS_DOCUMENT_DB or IS_KEY_VALUE_DB:

    @pytest.fixture(scope='function', autouse=True)
    async def engine():
        await initializeDB()