from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from src.config.settings import settings

engine = create_async_engine(
    url=settings.ORDERS_DATABASE_URL, future=True, pool_size=10, max_overflow=20
)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
