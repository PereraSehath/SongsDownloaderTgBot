from pyrogram import Client
import os

BOT_TOKEN = int(os.environ.get("BOT_TOKEN", "")
API_ID = int(os.environ.get("API_ID", "7"))
API_HASH = int(os.environ.get("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")

if __name__ == "__main__" :
    plugins = dict(
        root="plugins"
    )
    bot = Client(
        "SongsDownloaderTgBot",
        bot_token=BOT_TOKEN,
        api_hash=API_HASH,
        api_id=API_ID,
        plugins=plugins
    )
    bot.run()
© 2021 GitHub, Inc.
