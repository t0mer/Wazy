from telebot import types, TeleBot
from telebot.custom_filters import AdvancedCustomFilter
from telebot.callback_data import CallbackData, CallbackDataFilter
from loguru import logger
from confighandler import ConfigHandler
from routecalculator import RouteCalculator
import json


class BotHandler:
    def __init__(self):
        self.config = ConfigHandler().config
        self.bot_token = self.config.get('Telegram','bot.token')
        self.bot = TeleBot(self.bot_token)
        self.calculator=RouteCalculator()
    

        #Handle start/help command
        @self.bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            self.bot.send_message(chat_id=message.chat.id, text=str(self.config.get('Telegram','bot.welcome.message')), reply_markup=self.routes_keyboard(), parse_mode='Markdown')

        # ---------------- Handle the back button --------------------
        @self.bot.callback_query_handler(func=lambda c: c.data in json.loads(self.config.get('WAZE','routes')))
        def back_callback(call: types.CallbackQuery):
            time_in_minutes,route_time,distance,nav_url = self.calculator.get_route_info_by_name(call.data)
            message = "Current route status is: \n\n" \
              + "Distance: {}\n".format(distance) \
              + "Time to destination: {} ({} minutes)\n".format(route_time,time_in_minutes) \
              + "Navigation URL: {}\n".format(nav_url)
            self.bot.send_message(chat_id=call.message.chat.id, text=message)


    # -------------- Building kids selection inline keyboard
    def routes_keyboard(self):
        logger.debug("Build Routs Keyboard")
        markup = types.InlineKeyboardMarkup(row_width=1)
        result = []
        for route in json.loads(self.config.get('WAZE','routes')):
            markup.add(types.InlineKeyboardButton(
                text=route,
                callback_data=route))
            result.append(route)
        logger.debug("result:" + str(result))
        markup.add(types.InlineKeyboardButton(text=" ⬅ חזרה", callback_data="back"))
        return markup


    def start(self):
        try:
            logger.debug("Starting telegram bot")
            self.bot.infinity_polling()
        except Exception as e:
            logger.error(str(e))
