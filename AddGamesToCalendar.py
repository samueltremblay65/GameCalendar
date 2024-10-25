from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import timedelta
import os.path
import pickle

SCOPES = ['https://www.googleapis.com/auth/calendar']

def create_calendar(games):
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Feature 2: Create a new calendar
    new_calendar = {
        'summary': 'Ottawa Senators 2024-2025',
        'timeZone': '(GMT+02:00) Central European Time - Madrid'
    }

    created_calendar = service.calendars().insert(body=new_calendar).execute()
    print(f"Created calendar: {created_calendar['id']}")

    for game in games:
        # Feature 3: Insert an event
        event = {
            'summary': game.away + " @ " + game.home,
            'start': {
                'dateTime': (game.datetime).isoformat(),
                'timeZone': '(GMT-04:00) Eastern Time - Toronto',
            },
            'end': {
                'dateTime': (game.datetime + timedelta(hours=3)).isoformat(),
                'timeZone': '(GMT-04:00) Eastern Time - Toronto'
            },
        }

        created_event = service.events().insert(calendarId=created_calendar['id'], body=event).execute()
        print(f"Created event: {created_event['id']}")
