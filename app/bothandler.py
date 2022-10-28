from telebot import types, TeleBot
from telebot.custom_filters import AdvancedCustomFilter
from telebot.callback_data import CallbackData, CallbackDataFilter
from loguru import logger
from confighandler import ConfigHandler


class BotHandler:
    def __init__(self):
        self.config = ConfigHandler().config
        self.bot_token = self.config.get('Telegram','bot.token')
        self.bot = TeleBot(self.bot_token)
    

        #Handle start/help command
        @self.bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            self.bot.reply_to(message, self.config.get('Telegram','bot.welcome.message'))


    def start(self):
        self.bot.infinity_polling()