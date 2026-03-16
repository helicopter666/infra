from fastapi import APIRouter

# Импортировать роутеры конкретного сервиса здесь:
# from app.api.v1 import auth, jobs, schemas  # пример для TextExtract API

api_router = APIRouter()

# api_router.include_router(auth.router,    prefix="/auth",    tags=["auth"])
# api_router.include_router(jobs.router,    prefix="/jobs",    tags=["jobs"])
# api_router.include_router(schemas.router, prefix="/schemas", tags=["schemas"])
