from sqlalchemy import BigInteger
from sqlalchemy.orm import (Mapped,
                            mapped_column,
                            DeclarativeBase)


class Base(DeclarativeBase):
    pass


class VoiceMessage(Base):
    __tablename__ = "voice_message"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    file_id: Mapped[str] = mapped_column()
    path: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
