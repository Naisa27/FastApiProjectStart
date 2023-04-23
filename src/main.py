from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis
from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate

from src.operations.router import router as router_operation

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Service started")
    redis = aioredis.from_url( "redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init( RedisBackend( redis ), prefix="cache")
    yield
    print("Service exited")

app = FastAPI(
    title="Trading App",
    lifespan=lifespan
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_operation)

# @app.on_event("startup")
# async def startup():
#     print("=================================== я тут ================================")
#     redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
#     print("redis = ", redis)
#     FastAPICache.init(RedisBackend(redis), prefix="cache")
