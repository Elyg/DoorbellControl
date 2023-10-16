import os
import firebase_admin
from firebase_admin import credentials, credentials, firestore

class DoorBellState():
    def __init__(self, mode=True):
        self.mode = mode
        self.initialize()
        
    def initialize(self):  
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
        
        print("Setting mode from Firebase DB!")
        self.mode = mode=doc_ref.get().to_dict()['mode']
        
        print("Attaching changes listener!")
        doc_ref.on_snapshot(lambda x, y, z : self.query_modified(doc_snapshot=x, changes=y, read_time=z))

    def query_modified(self, doc_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'MODIFIED':
                print(u'Modified New Value: {}'.format(change.document.to_dict()))
                self.mode = change.document.to_dict()["mode"]
            
