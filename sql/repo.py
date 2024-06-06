from typing import Optional
from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio.session import AsyncSession

from sql.models import VoiceMessage


class UserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, message_id: int,
                     path: str, file_id: str) -> VoiceMessage:
        user = VoiceMessage(id=message_id)
        check = await self.get(message_id=message_id)
        if not check:
            self.session.add(user)
            await self.session.commit()
        return user

    async def get(self, message_id: int) -> Optional[VoiceMessage]:
        return await self.session.get(VoiceMessage, message_id)

    async def update(self, message_id: int, **kwargs) -> None:
        stmt = (update(VoiceMessage).
                where(VoiceMessage.id == message_id).
                values(**kwargs))
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete(self, message_id: int) -> None:
        stmt = delete(VoiceMessage).where(VoiceMessage.id == message_id)
        await self.session.execute(stmt)
        await self.session.commit()
