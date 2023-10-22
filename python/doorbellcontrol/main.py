import sys
from threading import Thread

from gpiozero import Button, DigitalOutputDevice
from signal import pause

from telegram_bot import DoorbellTelegramBot
from telegram_basic import send_telegram_message, get_other_tokens
from database import DoorBellState

from google_calendar_sync import sync_calendar

from custom_logger import setup_logger
logger = setup_logger(__name__, color="White")

logger.info(sys.executable)

GPIO_BUTTON = 2
GPIO_RELAY = 17

TELEGRAM_BOT_TOKEN = get_other_tokens("telegram_bot_token")
TELEGRAM_CHAT_ID = get_other_tokens("telegram_chat_id")

def relay_turn_on():
    if doorbell_state.mode:
        doorbell_state.device_relay.on() # relay .on() no bell
    print("Relay ON! {}".format(doorbell_state.device_relay.value))
    
def relay_turn_off():
    if doorbell_state.mode:
        doorbell_state.device_relay.off() # relay .off() ring bell 
    try:
        send_telegram_message(message=doorbell_state.phrase, token=TELEGRAM_BOT_TOKEN, chat_id=TELEGRAM_CHAT_ID)
    except Exception as e:
        print(e)
    print("Relay OFF! {}".format(doorbell_state.device_relay.value))
    
if __name__ == '__main__':
    
    device_relay = DigitalOutputDevice(pin=GPIO_RELAY, active_high=False)
    doorbell_state = DoorBellState(device_relay=device_relay)
    
    telegram_bot = DoorbellTelegramBot(doorbell_state=doorbell_state)
    
    logger.info("MODE: {}".format(doorbell_state.mode))
    logger.info("PHRASE: {}".format(doorbell_state.phrase))
    logger.info("USE CALENDAR: {}".format(doorbell_state.use_calendar))
    
    button = Button(GPIO_BUTTON)
    button.when_pressed = lambda : relay_turn_on(doorbell_state)
    button.when_released = lambda : relay_turn_off(doorbell_state)
    
    calendar_thread = Thread(target=lambda: sync_calendar(doorbell_state))
    calendar_thread.start()
    
    telegram_bot.run()
    calendar_thread.join()
    
    pause()

