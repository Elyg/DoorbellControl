import sys
import logging
from threading import Thread

from gpiozero import Button, DigitalOutputDevice
from signal import pause

from telegram_bot import DoorbellTelegramBot, run_telegram_bot
from telegram_basic import send_telegram_message, get_other_tokens
from database import DoorBellState

from google_calendar_sync import sync_calendar

# white
logging.basicConfig(
    format= "\033[37m"+'%(asctime)s - %(name)s - %(levelname)s - %(message)s'+"\033[0m",
    level=logging.INFO
)

logging.info(sys.executable)

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
        pass
        #send_telegram_message(message=doorbell_state.phrase, token=TELEGRAM_BOT_TOKEN, chat_id=TELEGRAM_CHAT_ID)
    except Exception as e:
        print(e)
    print("Relay OFF! {}".format(doorbell_state.device_relay.value))
    
if __name__ == '__main__':
    
    device_relay = DigitalOutputDevice(pin=GPIO_RELAY, active_high=False)
    
    doorbell_state = DoorBellState(device_relay=device_relay)
    telegram_bot = DoorbellTelegramBot(doorbell_state=doorbell_state)
    
    print("MODE: {}".format(doorbell_state.mode))
    print("PHRASE: {}".format(doorbell_state.phrase))
    print("USE CALENDAR: {}".format(doorbell_state.use_calendar))
    
    button = Button(GPIO_BUTTON)
    button.when_pressed = lambda : relay_turn_on(doorbell_state)
    button.when_released = lambda : relay_turn_off(doorbell_state)
    
    bot_thread = Thread(target=lambda: run_telegram_bot(telegram_bot))
    calendar_thread = Thread(target=lambda: sync_calendar(telegram_bot))
    
    bot_thread.start()
    calendar_thread.start()
    
    bot_thread.join()
    calendar_thread.join()
    
    pause()

