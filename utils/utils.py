from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.exceptions import TelegramBadRequest

from sql.repo import Repo
from config import settings


async def save_voice(bot: Bot, file_id: str, name: str):
    file = await bot.get_file(file_id=file_id)
    file_path = file.file_path
    await bot.download_file(file_path, f"voices/{name}.ogg")
    return f"voices/{name}.ogg"


async def check_voices(bot: Bot, repo: Repo):
    voices = await repo.get_all_voice_messages()
    for voice in voices:
        try:
            await bot.get_file(voice.file_id)
        except TelegramBadRequest:
            msg = await bot.send_voice(
                chat_id=settings.admin_id,
                voice=FSInputFile(path=voice.path))
            await repo.update(message_id=voice.id,
                              file_id=msg.voice.file_id)
