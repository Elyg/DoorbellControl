import sys
import os
import time

from gpiozero import Button, DigitalOutputDevice
from signal import pause

from telegram_bot import send_telegram_message
from database import DoorBellState
print(sys.executable)

DOORBELL_STATE = DoorBellState()
GPIO_BUTTON = 2
GPIO_RELAY = 17
DEVICE_RELAY = DigitalOutputDevice(pin=GPIO_RELAY, active_high=False)

def relay_turn_on():
    if DOORBELL_STATE.mode:
        DEVICE_RELAY.on() # relay .on() no bell
    print("Relay ON! {}".format(DEVICE_RELAY.value))
    
def relay_turn_off():
    if DOORBELL_STATE.mode:
        DEVICE_RELAY.off() # relay .off() ring bell 
    try:
        send_telegram_message(message="Doorbell rang!")
    except Exception as e:
        print(e)
    print("Relay OFF! {}".format(DEVICE_RELAY.value))
    

# sudo systemctl restart doorbell.service
# journalctl -u doorbell.service -f
print("MODE: {}".format(DOORBELL_STATE.mode))
button = Button(GPIO_BUTTON)
button.when_pressed = relay_turn_on
button.when_released = relay_turn_off

pause()
        

