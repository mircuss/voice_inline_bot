import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    bot_token: str = os.getenv("BOT_TOKEN")
    webhook_url: str = os.getenv("WEBHOOK_URL")
    db_url: str = os.getenv("DB_URL")
    admin_id: str = os.getenv("ADMIN_ID")


settings = Settings()
