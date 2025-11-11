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

    def __init__(self, *, project_id:int=0):
            
        Message.status = True
        telegram_conf_dict = config.get('telegram', None)
        if telegram_conf_dict is None:
            Message.status = False

        telegram_conf_def = telegram_conf_dict[0]
        project_id = project_id
        if project_id==0:    
            telegram_conf = telegram_conf_def
        else:
            telegram_conf_prj = telegram_conf_dict.get(0, {})
            telegram_conf = {**telegram_conf_prj, **telegram_conf_def}
        
        if self.status:
            telegram_api_token = telegram_conf.get('api_token', None)
            if telegram_api_token is None:
                Message.status = False

        if Message.status:        
            channels = telegram_conf.get('channels', None)
            if channels is None:
                Message.status = False
            
        if Message.status:      
            if telegram_api_token!='':
                Message.bot = telebot.TeleBot(telegram_api_token)

            self.log_channel = channels.get('log', '')
            self.err_channel = channels.get('error', '')
            self.critical_channel = channels.get('critical', '')
            self.important_channel = channels.get('important', '')
            self.all_channel = channels.get('all', '')
            self.news_channel = channels.get('news', '')

    @staticmethod
    def send(message_str:str, *, lvl:str='all', img_buf=None, project_id:int=0) -> int:
        "lvl: log | error | critical | important | all (default) | news"
        
        if not Message.status:
            return 0
        
        if Message.obj is None:
            Message.obj = Message(project_id=project_id)
        message = Message.obj    

        res = 0

        if lvl=='news' and message.news_channel!='':
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
        
        if lvl=='log' and message.log_channel!='' and message_str!='':
            logging.info(f"Try to send lvl: {lvl}, channel: {message.log_channel}, message: {message_str}")   
            try:
                msg_status = message.bot.send_message(message.log_channel, message_str)
                res += 1
            except:
                logging.warning("Messages send problems!")

        if lvl=='error' and message.err_channel!='' and message_str!='':
            logging.info(f"Try to send lvl: {lvl}, channel: {message.err_channel}, message: {message_str}")   
            try:
                msg_status = message.bot.send_message(message.err_channel, message_str)
                res += 1
            except:
                logging.warning("Messages send problems!")

        if lvl=='critical' and message.critical_channel!='':
            logging.info(f"Try to send lvl: {lvl}, channel: {message.critical_channel}, message: {message_str}")   
            try:
                if  message_str!='':
                    msg_status = message.bot.send_message(message.critical_channel, message_str, disable_web_page_preview=True,parse_mode='HTML')
                res += 1
                # if not img_buf is None:
                #     message.bot.send_photo(message.critical_channel, img_buf)
            except:
                logging.warning("Messages send problems!")

        if (lvl=='critical' or lvl=='important') and message.important_channel!='':
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

        if lvl!='error' and lvl!='log' and message.all_channel!='':
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
