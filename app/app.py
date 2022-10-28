import WazeRouteCalculator
from server import Server
from bothandler import BotHandler
from confighandler import ConfigHandler
from loguru import logger
import io
import os

os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['LANG'] = 'C.UTF-8'


server = Server()
bot = BotHandler()
# bot.start()

# conig = ConfigHandler().config
# logger.info(conig.sections())

server.start()
