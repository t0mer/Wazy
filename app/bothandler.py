import os
import sys
import time
import json
import schedule
from loguru import logger
from telebot import types, TeleBot
from confighandler import ConfigHandler
from routecalculator import RouteCalculator

class BotHandler:
    def __init__(self):
        logger.info("Initializing Telegram bot handler")
        self.config = ConfigHandler().config
        self.bot_token = self.config.get('Telegram','bot.token')
        self.bot = TeleBot(self.bot_token,True)
        self.calculator=RouteCalculator()
        self.run_scheduled_jobd=True
        self.message_id=0
    

        # --------- Handle start command and show list of configured routes ------------- #
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            logger.info("Start command received")
            self.message_id=self.bot.send_message(chat_id=message.chat.id, text=str(self.config.get('Telegram','bot.welcome.message')), reply_markup=self.routes_keyboard(), parse_mode='Markdown').message_id
            
         

        # ---------------- Check current route status -------------------- #
        @self.bot.callback_query_handler(func=lambda c: c.data in json.loads(self.config.get('WAZE','routes')))
        def routes_callback(call: types.CallbackQuery):
            logger.info("Checking travel time status for {}".format(call.data))
            time_in_minutes,route_time,distance,nav_url= self.calculator.get_route_info_by_name(call.data)
            max_duration = self.config.get(call.data,"route.max_duration")
            message = "Current status for <b>{}</b> route  is: \n\n".format(call.data) \
              + "Distance: {}\n".format(distance) \
              + "Time to destination: {} ({} minutes)\n".format(route_time,time_in_minutes) \
              + "Navigation URL: {}\n".format(nav_url)
            
            if int(time_in_minutes > int(max_duration)):
                message = message + "\n\n ⚠️ <b>The route travel time ({} Minutes) is longer then the maximum you set in approx {} minutes</b>".format(time_in_minutes,int(time_in_minutes)-int(max_duration))
            try:
                self.bot.delete_message(message_id=self.message_id, chat_id=call.message.chat.id)
            except:
                pass
            self.message_id=self.bot.send_message(chat_id=call.message.chat.id, text=message,parse_mode="html")
            self.message_id = self.bot.send_message(chat_id=call.message.chat.id, text="Would you like to schedule route time checkes?",reply_markup=self.yesno_keyboard(call.data), parse_mode='Markdown').message_id
            

        # ---------------- Set route check intervals --------------------
        @self.bot.callback_query_handler(func=lambda c: c.data.startswith('_'))
        def intervals_callback(call: types.CallbackQuery):
            logger.info("Setting route monitoring intervals")
            route_name = call.data.split(':')[0].replace('_','')
            interval = int(call.data.split(':')[1])
            try:
                self.bot.delete_message(message_id=self.message_id,chat_id=call.message.chat.id)
            except:
                pass
            self.message_id = self.bot.send_message(chat_id=call.message.chat.id,text="{} route will be checked every {} Minutes. \n".format(route_name,str(interval)),reply_markup=self.cancel_schedule_keyboard(), parse_mode='Markdown').message_id
            if self.run_scheduled_jobd==True:
                logger.debug("Stopping running schedulers before setting new one")
                self.run_scheduled_jobd=False
                schedule.clear()
                self.run_scheduled_jobd=True
                schedule.every(interval).minutes.do(self.schedule_check,route_name=route_name,chat_id=call.message.chat.id)
                logger.debug("Route traval monitoring scheduled to run every {} Minutes".format(str(interval)))
                while self.run_scheduled_jobd==True:
                    schedule.run_pending()
                    time.sleep(1)

# -------------- Handle cancel command ---------------- #
        @self.bot.callback_query_handler(lambda c: c.data == "Cancle")
        def intervals_clear_callback(call: types.CallbackQuery):
            logger.info("Canceling scheduled route monitoring")
            self.run_scheduled_jobd=False
            schedule.clear()
            self.bot.delete_message(message_id=self.message_id,chat_id=call.message.chat.id)
            self.bot.send_message(chat_id=call.message.chat.id, text="Route monitoring cancelled",parse_mode="html")

# -------------- Handle beck command ---------------- #
        @self.bot.callback_query_handler(lambda c: c.data == "Back")
        def intervals_clear_callback(call: types.CallbackQuery):
            try:
                self.bot.delete_message(message_id=self.message_id,chat_id=call.message.chat.id)
            except:
                pass

# -------------- Show interval keyboard ---------------- #
        @self.bot.callback_query_handler(func=lambda c: c.data.startswith('!'))
        def intervals_callback(call: types.CallbackQuery):
            message_id=0
            route_name = call.data.split(':')[1].replace('!','')
            action = call.data.split(':')[0].replace('!','')
            if action=="Yes":
                message_id = self.bot.send_message(chat_id=call.message.chat.id, text="Please select the check intervals",reply_markup=self.intervals_keyboard(route_name), parse_mode='Markdown').message_id
                self.bot.delete_message(message_id=self.message_id,chat_id=call.message.chat.id)
                
            try:
                self.bot.delete_message(message_id=self.message_id,chat_id=call.message.chat.id)
            except:
                pass
            self.message_id=message_id


# -------------- Cheduled route checks ---------------- #
    def schedule_check(self,route_name,chat_id):
        logger.debug("Checking route status")
        try:
            time_in_minutes,route_time,distance,nav_url= self.calculator.get_route_info_by_name(route_name)
            max_duration = self.config.get(route_name,"route.max_duration")
            message = "Current status for <b>{}</b> route  is: \n\n".format(route_name) \
                + "Distance: {}\n".format(distance) \
                + "Time to destination: {} ({} minutes)\n".format(route_time,time_in_minutes) \
                + "Navigation URL: {}\n".format(nav_url)
            
            if int(time_in_minutes > int(max_duration)):
                message = message + "\n\n ⚠️ <b>The route travel time ({} Minutes) is longer then the maximum you set by approx {} minutes</b>".format(time_in_minutes,int(time_in_minutes)-int(max_duration))
            self.bot.send_message(chat_id=chat_id, text=message,parse_mode="html")
        except Exception as e:
            logger.error("oh snap something went wrong. {}".format(e))





# -------------- Building routes menu keyboard ---------------- #
    def routes_keyboard(self):
        logger.debug("Build Routes Keyboard")
        markup = types.InlineKeyboardMarkup()
        markup.row_width=2
        for route in json.loads(self.config.get('WAZE','routes')):
            markup.add(types.InlineKeyboardButton(
                text=route,
                callback_data=route))
        return markup

# -------------- Building intervals menu keyboard ------------- #
    def intervals_keyboard(self,route):
        logger.debug("Building intervals menu")
        markup = types.InlineKeyboardMarkup()
        markup.row_width=3
        intervals= [5,10,15,20]
        for interval in intervals:
            markup.add(types.InlineKeyboardButton(
                text=str(interval) + " Minutes",
                callback_data="_{}:{}".format(route,interval)))
        markup.add(types.InlineKeyboardButton(
            text="Cancle",
            callback_data="Back"))
        return markup

# -------------- Building Yes/No action keyboard -------------- #
    def yesno_keyboard(self,route):
        logger.debug("Building Yes/No actions menu")
        markup = types.InlineKeyboardMarkup()
        markup.row_width=3
        actions= ['Yes','No']
        for action in actions:
            markup.add(types.InlineKeyboardButton(
                text=action,
                callback_data="!{}:{}".format(action,route)))
        return markup

# -------------- Building Cancel button ----------------------- #
    def cancel_schedule_keyboard(self):
        markup = types.InlineKeyboardMarkup()
        markup.row_width=3
        markup.add(types.InlineKeyboardButton(
            text="Cancle route monitor",
            callback_data="Cancle"))
        return markup


    def start(self):
        try:
            logger.debug("Starting telegram bot")
            self.bot.infinity_polling()
        except Exception as e:
            logger.error(str(e))

