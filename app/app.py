import io
import os
import sys
from server import Server
from loguru import logger
from bothandler import BotHandler
from confighandler import ConfigHandler
from multiprocessing.dummy import Process



os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['LANG'] = 'C.UTF-8'
logger.remove()
LOG_LEVEL = os.getenv("LOG_LEVEL")
logger.add(sys.stderr, level=LOG_LEVEL)

class Wazy:
    def __init__(self):
        self.config = ConfigHandler().config
        self.bot_enabled = self.config.get('Telegram','bot.enabled')


if __name__== "__main__":
    wazy = Wazy()
    wazy.server = Server()
    main_web = Process(target = wazy.server.start)
    main_web.start()

    if wazy.bot_enabled=="True":
        wazy.bot = BotHandler()
        main_bot = Process(target = wazy.bot.start)
        main_bot.start()
        main_bot.join()

    main_web.join()
    
