import time
import datetime

from custom_logger import setup_logger
logger = setup_logger(__name__, color="Green")

def sync_calendar(doorbell_state, bot_for_running=True):  

    logger.info("Initializing")
    doorbell = doorbell_state
    last_sync_hour = 0
    logger.info("Loop started")
    while bot_for_running.running:
        now = datetime.datetime.now()
        if (now.hour == 9 or now.hour == 23) and now.hour != last_sync_hour:
            doorbell.sync_calendar_to_firebase()
            last_sync_hour = now.hour
            logger.info("Google calendar synced {}".format(now))
        time.sleep(2)
    logger.info("Closing calendar sync loop!")