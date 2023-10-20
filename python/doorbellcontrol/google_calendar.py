import datetime
import pytz
from tzlocal import get_localzone
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

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
    
def get_calendar_events():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    creds = get_credentials()
    calendarId = 'i71m62sdv0scs65ecapi6dmcu2pq7p4s@import.calendar.google.com'
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
            print('No upcoming events found.')
            return
        
        
        date_format = "%Y-%m-%dT%H:%M:%SZ"  
        events_list = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            start = datetime.datetime.strptime(start, date_format)
            end = datetime.datetime.strptime(end, date_format) 

            # start_local = convert_datetime_to_local(start)
            # end_local = convert_datetime_to_local(end)
            
            # now = get_local_datetime() #+datetime.timedelta(hours=55)
            # print(now)
            # print(start, end, event['summary'])
            # print(start_local, end_local, event['summary'])
            # print(start_local < now < end_local)
            if "N" == event["summary"]:
                events_list.append(
                                    {"start": start,
                                    "end": end,
                                    "summary" : event['summary']
                                    }
                                )
            
        return events_list
            
    except HttpError as error:
        print('An error occurred: {}'.fromat(error))
        return []


