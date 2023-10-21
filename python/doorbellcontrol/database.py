import os
import firebase_admin
from firebase_admin import credentials, credentials, firestore
from google_calendar import create_calendar_events, get_calendar_events, get_local_datetime, convert_datetime_to_local

class DoorBellState():
    def __init__(self, mode=True):
        """_summary_

        Args:
            mode (bool, optional): Doorbell ring active or not. Defaults to True.
        """
        self._mode = mode
        self.phrase = "Doorbell Ring! Ring!"
        self.use_calendar = True
        self.calendar_events = []
        self.db = None
        self.initialize()
    
    @property
    def mode(self):
        """defines if doorbell should ring or not
        
        if calendar is in use, don't ring
        calendar events are queried from firebase db, UTC time

        Returns:
            bool: bell ring active or not
        """
        if self.use_calendar:
            time_now = get_local_datetime()
            for event in self.calendar_events:
                start = convert_datetime_to_local(event["start"])
                end = convert_datetime_to_local(event["end"])
                summary = event["summary"]
                if summary == "N" and start < time_now < end:
                    print("Calendar event in action!")
                    return False
                
            return self._mode
        else:
            return self._mode
        
    @mode.setter
    def mode(self, value):
        """set bell ring mode, which defines if bell should ring

        Args:
            value (bool): bool bell ring active or not
        """
        self._mode = value
    
    def is_event_in_action(self):
        """check if calendar blocking is in action

        Returns:
            bool: calendar blocking event in action or not
        """
        if self.use_calendar:
            time_now = get_local_datetime()
            for event in self.calendar_events:
                start = convert_datetime_to_local(event["start"])
                end = convert_datetime_to_local(event["end"])
                summary = event["summary"]
                if summary == "N" and start < time_now < end:
                    return (True, start, end)
        return (False, None, None)
    
    def initialize(self):
        """Connects to firebase realtime database
           Fetches all settings and calendar events and
           Sets the states for the members of the class
           
           Attaches a listener event, when firebase changes occur
           The class updates the values of it's memebers
        """
        # path to secret db
        json_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config", "secret.json")
        if os.path.exists(json_file_path):
            print("Secret exists!")
        else:
            print("Secret does not exist!")
            return  
        
        # Fetch the service account key JSON file contents
        cred = credentials.Certificate(json_file_path)
        firebase_admin.initialize_app(cred)

        # Create a reference to the Firestore database
        db = firestore.client()
        doc_ref = db.collection('settings').document("settings")
        calendar_ref = db.collection('settings').document("calendar")
        
        print("Setting mode from Firebase DB!")
        self.mode = doc_ref.get().to_dict()['mode']
        self.phrase = doc_ref.get().to_dict()['phrase']
        self.use_calendar = calendar_ref.get().to_dict()['use_calendar']
        self.calendar_events = calendar_ref.get().to_dict()["events"]
        
        print("Attaching changes listener!")
        doc_ref.on_snapshot(lambda x, y, z : self.query_modified(doc_snapshot=x, changes=y, read_time=z))
        calendar_ref.on_snapshot(lambda x, y, z : self.query_modified(doc_snapshot=x, changes=y, read_time=z, settings=False))
        
        self.db = db
        print("Reading google calendar!")
        self.sync_calendar_to_firebase()
        print("Found: {}".format(len(self.calendar_events)))
        
        
    def sync_calendar_to_firebase(self):
        """Queries google calendar and syncs it to the firebase database
        """
        create_calendar_events()
        self.calendar_events = get_calendar_events()
        self.db.collection('settings').document("calendar").update({"events" : self.calendar_events})
        self.calendar_events = self.db.collection('settings').document("calendar").get().to_dict()["events"]
        
    def query_modified(self, doc_snapshot, changes, read_time, settings=True):
        """_summary_

        Args:
            doc_snapshot (_type_): snapshot of firebase db document
            changes (_type_): what has changed in the database
            read_time (_type_): time of reading db
            settings (bool, optional): which changes to monitor. True = mode, phrase, False = use_calendar, events. Defaults to True.
        """
        for change in changes:
            if change.type.name == 'MODIFIED':
                print(u'Modified New Value: {}'.format(change.document.to_dict()))

                if settings:
                    self.mode = change.document.to_dict()["mode"]
                    self.phrase = change.document.to_dict()["phrase"]
                else:
                    self.use_calendar = change.document.to_dict()["use_calendar"]
                    self.calendar_events = change.document.to_dict()["events"]