from bot import config

import logging

import google.cloud.logging

from bot.bot import create_bot

# initialize logging
logging_client = google.cloud.logging.Client()
logging_client.get_default_handler()
logging_client.setup_logging(log_level=logging.DEBUG)
logging.info("Starting server...")

# enable monitoring
config.cloud_monitoring_enabled = True

# start the server
create_bot()
