import json
import datetime
import pytz
import logging
from tzlocal import get_localzone
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logging.basicConfig(
    format= "\033[35m"+'%(asctime)s - %(name)s - %(levelname)s - %(message)s'+"\033[0m",
    level=logging.INFO
)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_url(work=True):
    json_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config", "calendar.json")
    if json_file_path:
        with open(json_file_path, "r") as f:
            data = json.load(f)
            return data["calendar_work"] if work else data["calendar_personal"]
    return None

def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    
    token_json = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config", "token.json")
    credentials_json =  os.path.join(os.path.dirname(os.path.realpath(__file__)), "config", "credentials.json")
    if os.path.exists(token_json):
        creds = Credentials.from_authorized_user_file(token_json, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_json, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_json, 'w') as token:
            token.write(creds.to_json())
    return creds

def convert_datetime_to_local(datetime_utc):
    utc = pytz.timezone('UTC')
    local = get_localzone()
    return datetime_utc.replace(tzinfo=utc).astimezone(local)

def get_local_datetime():
    local = get_localzone()
    return datetime.datetime.now().replace(tzinfo=local)   
    
def get_calendar_events(work=False):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    creds = get_credentials()
    calendarId_work = get_calendar_url(work=True)
    calendar_personal = get_calendar_url(work=False)
    
    calendarId = calendarId_work if work else calendar_personal
    calendar_label = "N" if work else "Bell Off Auto"
    max_results = 10
    
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(calendarId=calendarId, timeMin=now,
                                              maxResults=max_results, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            logging.info('No upcoming events found.')
            return []
        
        if work:
            date_format = "%Y-%m-%dT%H:%M:%SZ"
        else:
            date_format = "%Y-%m-%dT%H:%M:%S%z"
        events_list = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            #print(start)
            #print(end)
            start = datetime.datetime.strptime(start, date_format)
            end = datetime.datetime.strptime(end, date_format) 

            if calendar_label == event["summary"]:
                events_list.append(
                                    {"start": start,
                                    "end": end,
                                    "summary" : event['summary']
                                    }
                                )
            
        return events_list
            
    except HttpError as error:
        logging.info('An error occurred: {}'.fromat(error))
        return []


def get_event_template(start, end, timezone, description='Doorbell is off', summary="Bell Off Auto"):
    event = {
        'summary': summary,
        'description': description,
        'start': 
            {
            'dateTime': start,
            'timeZone': timezone,
            },
        'end': 
            {
            'dateTime': end,
            'timeZone': timezone,
            }
        }
    return event

def create_calendar_events(calendar_events=None):
    creds = get_credentials()
    calendar_personal = get_calendar_url(work=False)
    calendarId = calendar_personal
    
    #max_results = 2
    
    try:
        service = build('calendar', 'v3', credentials=creds)

        work_calendar_events = get_calendar_events(work=True)
        personal_calendar_events = get_calendar_events(work=False)
        created_events = []
        for event in work_calendar_events:
            valid = True
            offset_start = datetime.timedelta(hours=9)
            offset_end = datetime.timedelta(hours=12)
            start = convert_datetime_to_local(event["start"]+offset_start)
            end = convert_datetime_to_local(event["end"]+offset_end)
            for personal_event in personal_calendar_events:
                personal_start = personal_event["start"]
                personal_end = personal_event["end"]
                if personal_start == start and personal_end == end:
                    valid = False
                    
            if not valid:
                logging.info("Duplicate: {}".format(event))
                continue
            
            logging.info("Creating event!")
            event_template = get_event_template(start=start.strftime("%Y-%m-%dT%H:%M:%S%z"), end=end.strftime("%Y-%m-%dT%H:%M:%S%z"), timezone=str(get_localzone()))
            new_event = service.events().insert(calendarId=calendarId, body=event_template).execute()
            created_events.append(new_event)
            
        return created_events
            
    except HttpError as error:
        logging.info('An error occurred: {}'.fromat(error))
        return []