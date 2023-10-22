import time
import datetime
import logging

logging.basicConfig(
    format= "\033[36m"+'%(asctime)s - %(name)s - %(levelname)s - %(message)s'+"\033[0m",
    level=logging.INFO
)

def sync_calendar(bot):  

    logging.info("Initializing")
    doorbell = bot.doorbell_state
    last_sync_hour = 0
    logging.info("Loop started")
    while True:
        now = datetime.datetime.now()
        if (now.hour == 9 or now.hour == 23) and now.hour != last_sync_hour:
            doorbell.sync_calendar_to_firebase()
            last_sync_hour = now.hour
            logging.info("Google calender synced {}".format(now))
        time.sleep(60*10)