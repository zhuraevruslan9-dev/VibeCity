import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_PATH = os.getenv("DATABASE_PATH", "vibecity.db")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is not set. Add it to your .env file or environment variables."
    )