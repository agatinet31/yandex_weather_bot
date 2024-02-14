from aiogram import Router

from .users import router as user_router


def setup_routers() -> Router:
    router = Router()
    router.include_router(user_router)

    return router
