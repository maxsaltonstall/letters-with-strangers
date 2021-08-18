import os, logging
import google.cloud.logging

from discord.ext import commands

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

logging.info("⚙️  Loading .env...")
load_dotenv(override=True)

if os.environ.get("DEPLOYMENT_CONTEXT", "local") == "gce":
    # start up Google Cloud Logging
    client = google.cloud.logging.Client()
    client.get_default_handler()
    client.setup_logging()
    logging.info("💻 Starting Server...")

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
    print(f"❗ Error while logging in: {e}")