import uuid
from aiogram import F, Router, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (Message, InlineQuery,
                           InlineQueryResultCachedVoice,
                           InputTextMessageContent)


from sql.repo import Repo
from utils import save_voice, check_voices
from states.voice_states import VoiceStates

from config import settings

voice_router = Router()


@voice_router.message(F.voice, F.from_user.id == int(settings.admin_id))
async def new_voice_message(message: Message, state: FSMContext):
    data = {"file_id": message.voice.file_id,
            "id": message.message_id}
    await state.set_state(VoiceStates.get_name)
    await state.update_data(data)
    await message.answer(text="Send me name")


@voice_router.message(StateFilter(VoiceStates.get_name),
                      F.from_user.id == int(settings.admin_id))
async def get_voice_name(message: Message, state: FSMContext,
                         repo: Repo, bot: Bot) -> None:
    data = await state.get_data()
    file_id = data["file_id"]
    message_id = data["id"]
    name = message.text
    path = await save_voice(bot=bot, name=name,
                            file_id=file_id)
    await repo.create(message_id=message_id,
                      path=path, file_id=file_id, name=name)
    await message.answer(text="SAVED SUCCESSFULLY")
    await state.clear()


@voice_router.inline_query(F.query == "/d",
                           F.from_user.id == int(settings.admin_id))
async def delete_voice(inline_query: InlineQuery, repo: Repo):
    results = []
    await check_voices(bot=inline_query.bot,
                       repo=repo)
    voices = await repo.get_all_voice_messages()
    for voice in voices:
        message_content = InputTextMessageContent(
            message_text=f"/d {voice.id}")
        results.append(
            InlineQueryResultCachedVoice(title=voice.name,
                                         id=str(uuid.uuid4()),
                                         voice_file_id=voice.file_id,
                                         input_message_content=message_content)
        )
    await inline_query.answer(results=results, cache_time=1, is_personal=True)


@voice_router.message(F.text.startswith("/d"))
async def delete_message(message: Message, repo: Repo):
    print(message.text)
    voice_id = message.text.split()[-1]
    await repo.delete(message_id=voice_id)
    await message.delete()
