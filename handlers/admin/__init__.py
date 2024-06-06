from aiogram import Router
from .voice import voice_router

admin_router = Router()
admin_router.include_router(voice_router)

__all__ = [admin_router]
