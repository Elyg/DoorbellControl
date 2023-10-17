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
/off - turn off doorbell
/status - bot responds if doorbell is on or off
    
/phrase 
bot responds you what current doorbell phrase is

/phrase *newPhrase*
bot sets newPhrase as the new phrase for the doorbell

/help - show this help message

"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode=constants.ParseMode.MARKDOWN)

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
    DOORBELL.db.collection('settings').document("settings").update({"mode" : True})
    await context.bot.send_message(chat_id=update.effective_chat.id, text="DOORBELL: ON")
    
    
async def turn_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    DOORBELL.db.collection('settings').document("settings").update({"mode" : False})
    await context.bot.send_message(chat_id=update.effective_chat.id, text="DOORBELL: OFF")
    
    
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = DOORBELL.db.collection('settings').document("settings").get().to_dict()["mode"]
    await context.bot.send_message(chat_id=update.effective_chat.id, text="DOORBELL: {}".format("ON" if mode else "OFF"))
    
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
    
    status_handler = CommandHandler('help', help)
    application.add_handler(status_handler)
    
    application.run_polling()