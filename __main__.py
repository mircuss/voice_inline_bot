import logging
import uvicorn
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

from contextlib import asynccontextmanager

from middlewares.db_middleware import DataBaseMiddelware

from handlers.user import user_router
from handlers.admin import admin_router

from sql.db import create_pool

from config import settings

WEBHOOK_PATH = f"/bot/{settings.bot_token}"
WEBHOOK_URL = settings.webhook_url + WEBHOOK_PATH

storage = MemoryStorage()
session_factory = create_pool(settings.db_url)

bot = Bot(token=settings.bot_token)
dp = Dispatcher(storage=storage)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(url=WEBHOOK_URL)

    yield
    await bot.delete_webhook()

app = FastAPI(lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)


def register_middlewares(dp: Dispatcher) -> Dispatcher:
    dp.update.outer_middleware(DataBaseMiddelware(session_factory))
    return dp


def register_routers(dp: Dispatcher) -> Dispatcher:
    dp.include_router(admin_router)
    dp.include_router(user_router)
    return dp


def main():
    register_routers(dp=dp)
    register_middlewares(dp=dp)
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
    logging.basicConfig(filemode='a', level=logging.INFO)
