import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Full read/write scope
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_calendar():
    creds = None
    token_path = 'calendar_integration/token.json'
    creds_path = 'calendar_integration/credentials.json'

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service

def get_upcoming_events(n=5):
    service = authenticate_google_calendar()
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # UTC time
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        maxResults=n,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    if not events:
        return "No upcoming events found."
    event_list = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        event_list.append(f"{start} - {event['summary']}")
    return "\n".join(event_list)

def create_event(summary: str, start_time: datetime.datetime, duration_minutes: int = 60):
    service = authenticate_google_calendar()

    end_time = start_time + datetime.timedelta(minutes=duration_minutes)
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Europe/Berlin',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Europe/Berlin',
        },
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    return f"Event created: {created_event.get('htmlLink')}"
