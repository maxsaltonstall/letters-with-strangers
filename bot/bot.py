import os, logging

from discord.ext import commands

from dotenv import load_dotenv

load_dotenv(override=True)
logging.basicConfig(level=os.environ.get("LOG_LEVEL", logging.INFO))


def create_bot():
    bot = commands.Bot(
        command_prefix='..', description='''A bot to help strangers make words out of letters''',
    )

    logging.info("⚙️  Loading cogs...")
    for file in os.listdir("bot/cogs"):
        if file.endswith(".py"):
            bot.load_extension(f"bot.cogs.{file[:-3]}")

    logging.info("🔑 Logging in...")
    try:
        bot.run(os.environ["TOKEN"])
    except Exception as e:
        logging.critical(f"❗ Critical error while logging in: {e}")
