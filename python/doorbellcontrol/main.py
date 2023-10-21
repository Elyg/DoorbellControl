import sys
import os
import time

from gpiozero import Button, DigitalOutputDevice
from signal import pause

from telegram_basic import send_telegram_message, get_other_tokens
from database import DoorBellState
print(sys.executable)

DOORBELL_STATE = DoorBellState()
GPIO_BUTTON = 2
GPIO_RELAY = 17
DEVICE_RELAY = DigitalOutputDevice(pin=GPIO_RELAY, active_high=False)

TELEGRAM_BOT_TOKEN = get_other_tokens("telegram_bot_token")
TELEGRAM_CHAT_ID = get_other_tokens("telegram_chat_id")

def relay_turn_on():
    if DOORBELL_STATE.mode:
        DEVICE_RELAY.on() # relay .on() no bell
    print("Relay ON! {}".format(DEVICE_RELAY.value))
    
def relay_turn_off():
    if DOORBELL_STATE.mode:
        DEVICE_RELAY.off() # relay .off() ring bell 
    try:
        send_telegram_message(message=DOORBELL_STATE.phrase, token=TELEGRAM_BOT_TOKEN, chat_id=TELEGRAM_CHAT_ID)
    except Exception as e:
        print(e)
    print("Relay OFF! {}".format(DEVICE_RELAY.value))
    
def main():
    print("MODE: {}".format(DOORBELL_STATE.mode))
    print("PHRASE: {}".format(DOORBELL_STATE.phrase))
    print("USE CALENDAR: {}".format(DOORBELL_STATE.use_calendar))
    button = Button(GPIO_BUTTON)
    button.when_pressed = relay_turn_on
    button.when_released = relay_turn_off

    pause()
    
if __name__ == '__main__':
    main()

