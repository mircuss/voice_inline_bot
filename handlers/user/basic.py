from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

basic_router = Router()


@basic_router.message(F.text == "/start")
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()
    return await message.answer(text="Hi!")
