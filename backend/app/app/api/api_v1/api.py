from fastapi import APIRouter

from app.api.api_v1.endpoints import items, login, users, utils, companies, branches, cars, user_interaction

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(branches.router, tags=["branches"])
api_router.include_router(cars.router, tags=["cars"])
api_router.include_router(user_interaction.router, tags=["user_interactions"])
