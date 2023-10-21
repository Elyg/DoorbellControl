import time
import datetime
from database import DoorBellState

def main():
    """Syncs google calendar to firebase
    every day at 9:00 and 23:00
    """
    print("Initializing")
    doorbell = DoorBellState()
    last_sync_hour = 0
    print("Loop started")
    while True:
        now = datetime.datetime.now()
        if (now.hour == 9 or now.hour == 23) and now.hour != last_sync_hour:
            doorbell.sync_calendar_to_firebase()
            last_sync_hour = now.hour
            print("Google calender synced {}".format(now))
        time.sleep(60*10)
        
if __name__ == '__main__':
    main()