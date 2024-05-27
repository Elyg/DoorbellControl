import os
import json
import asyncio
import time
import logging
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from custom_logger import setup_logger

setup_logger("", color="White")
setup_logger("httpx", color="Blue",level=logging.WARNING)
logger = setup_logger(__file__, color="Blue")

def get_other_tokens(name):
    json_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config", "other_tokens.json")
    if json_file_path:
        with open(json_file_path, "r") as f:
            data = json.load(f)
            return data[name]
    return None

class DoorbellTelegramBot():
    def __init__(self, doorbell_state=None):
        bot_token = get_other_tokens("telegram_bot_token")
        application = ApplicationBuilder().token(bot_token).build()
        
        turn_on_handler = CommandHandler('on', self.turn_on)
        application.add_handler(turn_on_handler)
        
        turn_off_handler = CommandHandler('off', self.turn_off)
        application.add_handler(turn_off_handler)
        
        status_handler = CommandHandler('status', self.status)
        application.add_handler(status_handler)
        
        status_handler = CommandHandler('chat_id', self.chat_id)
        application.add_handler(status_handler)

        status_handler = CommandHandler('phrase', self.phrase)
        application.add_handler(status_handler)

        status_handler = CommandHandler('force_sync_calendar', self.force_sync_calendar)
        application.add_handler(status_handler)
        
        status_handler = CommandHandler('ring', self.ring)
        application.add_handler(status_handler)
        
        status_handler = CommandHandler('help', self.help)
        application.add_handler(status_handler)

        self.application = application
        self.doorbell_state = doorbell_state
        
        self.running = True

    async def ring(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        melody = False
        n = 1
        if len(context.args) > 0 and " ".join(context.args).lstrip():
            arg = " ".join(context.args).lstrip()
            logger.info(arg)
            if arg == "melody":
                melody = True
            if arg.isdigit():
                n = int(arg)
                
        self.doorbell_state.ring(times=n, melody=melody)
            
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        
        msg="""Available commands for the home bot 🏠:

    /on - turn on doorbell
    /on calendar - turn on calendar events to override the bell

    /off - turn off doorbell
    /off calendar - turn off the use of calendar

    /status - prints the settings if bell and calendar is active
        
    /phrase 
    prints the current doorbell phrase

    /phrase *newPhrase*
    bot sets newPhrase as the new phrase for the doorbell

    /force\_sync\_calendar - syncs the calendar events (syncs automatically happen 2 times in a day at 9:00 and 23:00)
    
    /ring - ring the doorbell once
    /ring n - ring the doorbell n times (capped at 5)
    /ring melody - ring the doorbell melody
    
    /chat\_id - get id of telegram chat for debug purpose

    /help - show this help message

    """
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode=constants.ParseMode.MARKDOWN)
        
    async def force_sync_calendar(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.doorbell_state.sync_calendar_to_firebase()
        events = self.doorbell_state.db.collection('settings').document("calendar").get().to_dict()["events"]
        use_calendar = self.doorbell_state.db.collection('settings').document("calendar").get().to_dict()["use_calendar"]
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Calendar Sync Done!\nEvents set {}\nUSE CALENDAR STATUS: {}".format(len(events),  "ON" if use_calendar else "OFF")) 
        
    async def chat_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="CHAT ID:\n\n{}".format(update.effective_chat.id)) 
        
    async def phrase(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if len(context.args) > 0 and " ".join(context.args).lstrip():
            phrase = " ".join(context.args).lstrip()
            self.doorbell_state.db.collection('settings').document("settings").update({"phrase" : phrase})
            await context.bot.send_message(chat_id=update.effective_chat.id, text="NEW DOORBELL PHRASE:\n\n{}".format(phrase))
        else:
            phrase = self.doorbell_state.db.collection('settings').document("settings").get().to_dict()["phrase"]
            await context.bot.send_message(chat_id=update.effective_chat.id, text="CURRENT DOORBELL PHRASE:\n\n{}".format(phrase))
       
    async def turn_on(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        set_calendar = False
        if len(context.args) > 0 and " ".join(context.args).lstrip():
            if "calendar" == context.args[0].lstrip():
                set_calendar = True
        if set_calendar:
            self.doorbell_state.db.collection('settings').document("calendar").update({"use_calendar" : True})
            await context.bot.send_message(chat_id=update.effective_chat.id, text="USE CALENDAR: ON")
        else:
            self.doorbell_state.db.collection('settings').document("settings").update({"mode" : True})
            await context.bot.send_message(chat_id=update.effective_chat.id, text="DOORBELL: ON")
        
    async def turn_off(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        set_calendar = False
        if len(context.args) > 0 and " ".join(context.args).lstrip():
            if "calendar" == context.args[0].lstrip():
                set_calendar = True
        if set_calendar:
            self.doorbell_state.db.collection('settings').document("calendar").update({"use_calendar" : False})
            await context.bot.send_message(chat_id=update.effective_chat.id, text="USE CALENDAR: OFF")
        else:
            self.doorbell_state.db.collection('settings').document("settings").update({"mode" : False})
            await context.bot.send_message(chat_id=update.effective_chat.id, text="DOORBELL: OFF")
        
        
    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        mode = self.doorbell_state.db.collection('settings').document("settings").get().to_dict()["mode"]
        use_calendar = self.doorbell_state.db.collection('settings').document("calendar").get().to_dict()["use_calendar"]
        door_status = "ON" if mode else "OFF"
        event_in_action, start, end = self.doorbell_state.is_event_in_action()
        if event_in_action and use_calendar and mode == True:
            door_status = "OFF (by calendar)\n{} - {}\n".format(start.strftime("%Y-%m-%d %H:%M"), end.strftime("%Y-%m-%d %H:%M")) if event_in_action else "ON"

        await context.bot.send_message(chat_id=update.effective_chat.id, text="DOORBELL: {}\nUSE CALENDAR: {}".format(door_status, "ON" if use_calendar else "OFF"))
    
    def run(self):
        self.running = True
        logger.info("1. Starting telegram bot...")
        self.application.run_polling()
        logger.info("2. Ending telegram bot...")
        self.running = False
