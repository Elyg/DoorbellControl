import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from database import DoorBellState

DOORBELL = DoorBellState()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def turn_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    DOORBELL.db.collection('settings').document("settings").set({"mode" : True})
    await context.bot.send_message(chat_id=update.effective_chat.id, text="DOORBELL: ON")
    
async def turn_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    DOORBELL.db.collection('settings').document("settings").set({"mode" : False})
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
    
    application.run_polling()