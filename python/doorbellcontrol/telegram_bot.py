import logging
import os
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from database import DoorBellState

DOORBELL = DoorBellState()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    msg="""Available commands for the home bot 🏠:

/on - turn on doorbell
/on calendar - turn on use of calendar for doorbell activation

/off - turn off doorbell
/off calendar - turn off use of calendar for doorbell activation

/status - bot responds if doorbell is on or off or calendar is in use
    
/phrase 
bot responds you what current doorbell phrase is

/phrase *newPhrase*
bot sets newPhrase as the new phrase for the doorbell

/force\_sync\_calendar - forces to sync calendar update usually calendar gets synced every 2 times every day 9 00 and 23 00

/chat\_id - get id of telegram chat for debug purpose

/help - show this help message

"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode=constants.ParseMode.MARKDOWN)
    
async def force_sync_calendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    DOORBELL.sync_calendar_to_firebase()
    events = DOORBELL.db.collection('settings').document("calendar").get().to_dict()["events"]
    use_calendar = DOORBELL.db.collection('settings').document("calendar").get().to_dict()["use_calendar"]
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Calendar Sync Done!\nEvents set {}\nUSE CALENDAR STATUS: {}".format(len(events),  "ON" if use_calendar else "OFF")) 
    
async def chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="CHAT ID:\n\n{}".format(update.effective_chat.id)) 
    
async def phrase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) > 0 and " ".join(context.args).lstrip():
        phrase = " ".join(context.args).lstrip()
        DOORBELL.db.collection('settings').document("settings").update({"phrase" : phrase})
        await context.bot.send_message(chat_id=update.effective_chat.id, text="NEW DOORBELL PHRASE:\n\n{}".format(phrase))
    else:
        phrase = DOORBELL.db.collection('settings').document("settings").get().to_dict()["phrase"]
        await context.bot.send_message(chat_id=update.effective_chat.id, text="CURRENT DOORBELL PHRASE:\n\n{}".format(phrase))
 
        
async def turn_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    set_calendar = False
    if len(context.args) > 0 and " ".join(context.args).lstrip():
        if "calendar" == context.args[0].lstrip():
            set_calendar = True
    if set_calendar:
        DOORBELL.db.collection('settings').document("calendar").update({"use_calendar" : True})
        await context.bot.send_message(chat_id=update.effective_chat.id, text="USE CALENDAR: ON")
    else:
        DOORBELL.db.collection('settings').document("settings").update({"mode" : True})
        await context.bot.send_message(chat_id=update.effective_chat.id, text="DOORBELL: ON")
    
    
async def turn_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    set_calendar = False
    if len(context.args) > 0 and " ".join(context.args).lstrip():
        if "calendar" == context.args[0].lstrip():
            set_calendar = True
    if set_calendar:
        DOORBELL.db.collection('settings').document("calendar").update({"use_calendar" : False})
        await context.bot.send_message(chat_id=update.effective_chat.id, text="USE CALENDAR: OFF")
    else:
        DOORBELL.db.collection('settings').document("settings").update({"mode" : False})
        await context.bot.send_message(chat_id=update.effective_chat.id, text="DOORBELL: OFF")
    
    
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = DOORBELL.db.collection('settings').document("settings").get().to_dict()["mode"]
    use_calendar = DOORBELL.db.collection('settings').document("calendar").get().to_dict()["use_calendar"]
    
    door_status = "ON" if mode else "OFF"
    event_in_action, start, end = DOORBELL.is_event_in_action()
    if event_in_action and use_calendar and mode == True:
        door_status = "OFF (by calendar)\n{} - {}\n".format(start.strftime("%Y-%m-%d %H:%M"), end.strftime("%Y-%m-%d %H:%M")) if event_in_action else "ON"

    await context.bot.send_message(chat_id=update.effective_chat.id, text="DOORBELL: {}\nUSE CALENDAR: {}".format(door_status, "ON" if use_calendar else "OFF"))
    
if __name__ == '__main__':
    application = ApplicationBuilder().token("***REMOVED***").build()
    
    turn_on_handler = CommandHandler('on', turn_on)
    application.add_handler(turn_on_handler)
    
    turn_off_handler = CommandHandler('off', turn_off)
    application.add_handler(turn_off_handler)
    
    status_handler = CommandHandler('status', status)
    application.add_handler(status_handler)
    
    status_handler = CommandHandler('chat_id', chat_id)
    application.add_handler(status_handler)

    status_handler = CommandHandler('phrase', phrase)
    application.add_handler(status_handler)

    status_handler = CommandHandler('force_sync_calendar', force_sync_calendar)
    application.add_handler(status_handler)
    
    status_handler = CommandHandler('help', help)
    application.add_handler(status_handler)
    
    application.run_polling()