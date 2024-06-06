from aiogram import F, Router
from aiogram.types import Message


basic_router = Router()


@basic_router.message(F.text == "/start")
async def start_cmd(message: Message):
    return await message.answer(text="Hi!")
