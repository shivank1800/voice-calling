import datetime
from cal_setup import get_calendar_service
calID = "ed8d464d2e7e1f6662f9d569119fa648b9c28eebc2c8e15044d47d07bf116eaa@group.calendar.google.com"
def create_event(starttime, endtime):
    service = get_calendar_service()
    event = {
    'description': 'Appointment',
    'start': {
        'dateTime': starttime,
        'timeZone': 'Asia/Kolkata',
    },
    'end': {
        'dateTime': endtime,
        'timeZone': 'Asia/Kolkata',
    }
    }

    event = service.events().insert(calendarId=calID, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))