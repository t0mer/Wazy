import WazeRouteCalculator
from server import Server
from bothandler import BotHandler
from confighandler import ConfigHandler
from loguru import logger
import io
import os

os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['LANG'] = 'C.UTF-8'
config = ConfigHandler().config


if bool(config.get('Telegram','bot.enabled')):
    bot = BotHandler()
    bot.start()


# server = Server()
# server.start()
