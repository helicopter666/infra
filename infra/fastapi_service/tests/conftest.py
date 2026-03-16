import pytest
import pytest_asyncio
import fakeredis.aioredis as fakeredis
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.main import app
from app.db.base import Base
from app.core.dependencies import get_db, get_redis

# ── Тестовая БД (SQLite in-memory для unit-тестов, Postgres для integration) ──

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine):
    factory = async_sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)
    async with factory() as session:
        yield session
        await session.rollback()


@pytest.fixture
def fake_redis():
    return fakeredis.FakeRedis(decode_responses=True)


@pytest_asyncio.fixture
async def client(db_session, fake_redis):
    app.dependency_overrides[get_db] = lambda: db_session
    app.dependency_overrides[get_redis] = lambda: fake_redis
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


# ── Вспомогательные фабрики (переопределяются в конкретном проекте) ───────────

@pytest.fixture
def make_user():
    """Переопределить в конкретном проекте."""
    raise NotImplementedError


@pytest.fixture
def auth_headers(make_user):
    """Переопределить в конкретном проекте."""
    raise NotImplementedError
