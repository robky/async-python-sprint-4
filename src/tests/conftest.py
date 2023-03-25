import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from db.database import Base, engine
from main import app


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncSession:
    session = async_sessionmaker(engine, expire_on_commit=False)

    async with session():
        async with engine.begin() as connect:
            await connect.run_sync(Base.metadata.create_all)

        yield session

    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope="function")
def prefix_shorten() -> str:
    return "/api/v1/shorten"


@pytest.fixture(scope="function")
def link_test_data() -> dict:
    return {"original_url": "yandex.ru", "full_url": "http://yandex.ru"}


@pytest.fixture(scope="function")
def link_bulk_test_data() -> list[dict]:
    return [
        {"original_url": "one.com"},
        {"original_url": "two.com"},
        {"original_url": "three.com"}
    ]
