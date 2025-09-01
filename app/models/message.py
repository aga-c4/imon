import telebot
import logging
from time import sleep

from config import config

class Message():
    status = True
    obj = None

    bot = None
    log_chanel = None
    err_channel = None
    critica_channel = None
    important_channel = None
    all_channel = None
    news_channel = None

    def __init__(self):
        Message.status = True
        telegram_conf = config.get('telegram', None)
        if telegram_conf is None:
            Message.status = False
        
        if self.status:
            telegram_api_token = telegram_conf.get('api_token', None)
            if telegram_api_token is None:
                Message.status = False

        if Message.status:        
            channels = telegram_conf.get('channels', None)
            if channels is None:
                Message.status = False
            
        if Message.status:    
            Message.bot = telebot.TeleBot(telegram_api_token)

            self.log_channel = channels.get('log', None)
            self.err_channel = channels.get('error', None)
            self.critical_channel = channels.get('critical', None)
            self.important_channel = channels.get('important', None)
            self.all_channel = channels.get('all', None)
            self.news_channel = channels.get('news', None)

    @staticmethod
    def send(message_str:str, *, lvl:str='all', img_buf=None) -> int:
        "lvl: log | error | critical | important | all (default) | news"
        
        if not Message.status:
            return 0
        
        if Message.obj is None:
            Message.obj = Message()
        message = Message.obj    

        res = 0

        if lvl=='news' and not message.news_channel is None:
            logging.info(f"Try to send lvl: {lvl}, channel: {message.news_channel}, message: {message_str}")   
            try:
                if  message_str!='':
                    msg_status = message.bot.send_message(message.news_channel, message_str, disable_web_page_preview=True,parse_mode='HTML')
                res += 1
                if not img_buf is None:
                    sleep(1)
                    message.bot.send_photo(message.news_channel, img_buf)
            except:
                logging.warning("Messages send problems!")
            return res    
        
        if lvl=='log' and not message.log_channel is None and message_str!='':
            logging.info(f"Try to send lvl: {lvl}, channel: {message.log_channel}, message: {message_str}")   
            try:
                msg_status = message.bot.send_message(message.log_channel, message_str)
                res += 1
            except:
                logging.warning("Messages send problems!")

        if lvl=='error' and not message.err_channel is None and message_str!='':
            logging.info(f"Try to send lvl: {lvl}, channel: {message.err_channel}, message: {message_str}")   
            try:
                msg_status = message.bot.send_message(message.err_channel, message_str)
                res += 1
            except:
                logging.warning("Messages send problems!")

        if lvl=='critical' and not message.critical_channel is None:
            logging.info(f"Try to send lvl: {lvl}, channel: {message.critical_channel}, message: {message_str}")   
            try:
                if  message_str!='':
                    msg_status = message.bot.send_message(message.critical_channel, message_str, disable_web_page_preview=True,parse_mode='HTML')
                res += 1
                # if not img_buf is None:
                #     message.bot.send_photo(message.critical_channel, img_buf)
            except:
                logging.warning("Messages send problems!")

        if (lvl=='critical' or lvl=='important') and not message.important_channel is None:
            logging.info(f"Try to send lvl: {lvl}, channel: {message.important_channel}, message: {message_str}")   
            try:
                if  message_str!='':
                    msg_status = message.bot.send_message(message.important_channel, message_str, disable_web_page_preview=True, parse_mode='HTML')
                res += 1
                if res<3 and not img_buf is None:
                    sleep(1)
                    message.bot.send_photo(message.important_channel, img_buf)
            except:
                logging.warning("Messages send problems!")

        if lvl!='error' and lvl!='log' and not message.all_channel is None:
            logging.info(f"Try to send  lvl: {lvl}, channel: {message.all_channel}, message: {message_str}")   
            try:    
                if  message_str!='':
                    msg_status = message.bot.send_message(message.all_channel, message_str, disable_web_page_preview=True, parse_mode='HTML')
                if lvl!='critical' and lvl!='important':
                    res += 1
                if res<3 and not img_buf is None:
                    sleep(1)
                    message.bot.send_photo(message.all_channel, img_buf)
            except:
                logging.warning("Messages send problems!")

        return res
