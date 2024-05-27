import sys
import os
from threading import Thread
import subprocess

from gpiozero import Button, DigitalOutputDevice
import signal
from signal import pause

from telegram_bot import DoorbellTelegramBot
from telegram_basic import send_telegram_message, get_other_tokens
from database import DoorBellState
from google_calendar_sync import sync_calendar
from custom_logger import setup_logger

from datetime import datetime


logger = setup_logger(__name__, color="Cyan")
logger.info(sys.executable)

GPIO_BUTTON = 21 # power surge killed original GPIO2, seems like GPIO 21 WORKS though
GPIO_RELAY = 17

TELEGRAM_BOT_TOKEN = get_other_tokens("telegram_bot_token")
TELEGRAM_CHAT_ID = get_other_tokens("telegram_chat_id")

DEBUG = True

def shutdown_rpi():
    try:
        # The 'shutdown now' command will immediately shut down the Raspberry Pi
        subprocess.run(['sudo', 'shutdown', 'now'], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(e)

class DoorButton():
    def __init__(self, doorbell_state=None):
        self.doorbell_state = doorbell_state
        self.hold_time = 5
        self.button = Button(GPIO_BUTTON, hold_time=self.hold_time, hold_repeat=True)
        
        self.button.when_pressed = self.relay_turn_on
        self.button.when_released = self.relay_turn_off
        self.button.when_held = self.relay_auto_turn_off
        
        self.hold_counter = 0 
        self.max_hold_counts = 3
        
        self.press_counter = 0
        self.max_button_presses = 20
        
        self.reset_auto_safety_sec = 60.0
        
        self.last_hold_time = None
        self.last_on_time = None
        
        logger.info("Door Button initialized!")
            
    def relay_auto_turn_off(self):
        
        time_now = datetime.now()
        if self.last_hold_time == None:
           self.last_hold_time = time_now    
        elif (time_now - self.last_hold_time).total_seconds() >= self.reset_auto_safety_sec:
            self.hold_counter = 0
            self.last_hold_time = time_now
            
        if self.hold_counter < self.max_hold_counts:
            self.hold_counter += 1
            logger.info("Hold counter: {}/{}".format(self.hold_counter, self.max_hold_counts))
            
        if self.hold_counter >= self.max_hold_counts:
            extra_message = "Button was held {} times, at least {} seconds each time, in the span of {} seconds!".format(self.max_hold_counts, self.hold_time, self.reset_auto_safety_sec)
            self.emergency_turn_off(extra_message=extra_message)
            logger.info("Emergency relay shuttdown - from button press hold!")
            logger.info(extra_message)
        
    def relay_turn_on(self):
        time_now = datetime.now()
        if self.last_on_time == None:
           self.last_on_time = time_now 
        elif (time_now - self.last_on_time).total_seconds() >= self.reset_auto_safety_sec:
            self.press_counter = 0
            self.last_on_time = time_now
        
        if self.press_counter < self.max_button_presses:
            self.press_counter += 1
            logger.info("Button press counter: {}/{}".format(self.press_counter, self.max_button_presses))
            
        if self.press_counter >= self.max_button_presses:
            extra_message = "Button was pressed {} times in {} second span!".format(self.max_button_presses, self.reset_auto_safety_sec)
            self.emergency_turn_off(extra_message="Button was pressed {} times in {} second span!".format(self.max_button_presses, self.reset_auto_safety_sec))
            logger.info("Emergency relay shuttdown - from button press spams!")
            logger.info(extra_message)
            
        if self.doorbell_state.mode:
            if not DEBUG:
                self.doorbell_state.device_relay.on() # relay .on() no bell
        logger.info("Relay ON! {}".format(self.doorbell_state.device_relay.value))
        
    def relay_turn_off(self):
        if self.doorbell_state.mode:
            if not DEBUG:
                self.doorbell_state.device_relay.off() # relay .off() ring bell 
        try:
            if not DEBUG:
                send_telegram_message(message=self.doorbell_state.phrase, token=TELEGRAM_BOT_TOKEN, chat_id=TELEGRAM_CHAT_ID)
        except Exception as e:
            logger.error(e)
        logger.info("Relay OFF! {}".format(self.doorbell_state.device_relay.value))
    
    def emergency_turn_off(self, extra_message=""):
        if self.doorbell_state.device_relay.value:
            self.doorbell_state.device_relay.off()
        try:
            if not DEBUG:
                send_telegram_message(message="Emergency shutdown initiated! - {}".format(extra_message), token=TELEGRAM_BOT_TOKEN, chat_id=TELEGRAM_CHAT_ID)
        except Exception as e:
            logger.error(e)
        shutdown_rpi()
    
if __name__ == '__main__':
    
    device_relay = DigitalOutputDevice(pin=GPIO_RELAY, active_high=False)
    doorbell_state = DoorBellState(device_relay=device_relay)
    
    telegram_bot = DoorbellTelegramBot(doorbell_state=doorbell_state)
    
    logger.info("MODE: {}".format(doorbell_state.mode))
    logger.info("PHRASE: {}".format(doorbell_state.phrase))
    logger.info("USE CALENDAR: {}".format(doorbell_state.use_calendar))
    
    door_button = DoorButton(doorbell_state)
    
    calendar_thread = Thread(target=lambda: sync_calendar(doorbell_state, bot_for_running=telegram_bot))
    calendar_thread.daemon = True 
    calendar_thread.start()
    
    telegram_bot.run()
    calendar_thread.join()
    os.kill(os.getpid(), signal.SIGUSR1)
    pause()
    logger.info("Shutdown!")

