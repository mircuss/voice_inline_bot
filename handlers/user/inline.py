import uuid
from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultCachedVoice

from sql.repo import Repo
from utils import check_voices

inline_router = Router()


@inline_router.inline_query()
async def inline_action(inline_query: InlineQuery, repo: Repo):
    results = []
    data = inline_query.query.lower()
    await check_voices(bot=inline_query.bot,
                       repo=repo)
    voices = await repo.get_all_voice_messages()
    for voice in voices:
        if data in voice.name.lower() or inline_query.query == "":
            results.append(InlineQueryResultCachedVoice(
                title=voice.name,
                id=str(uuid.uuid4()),
                voice_file_id=voice.file_id
            ))
    await inline_query.answer(results=results, cache_time=1, is_personal=False)
