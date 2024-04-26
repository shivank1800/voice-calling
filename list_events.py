import datetime
from cal_setup import get_calendar_service
calID = "796b9a6fe7e4d74b8a5b119947f2e25ead07048e4093a270f38f0faed6e90855@group.calendar.google.com"
def main():
   service = get_calendar_service()
   # Call the Calendar API
   now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
   print('Getting List o 10 events')
   events_result = service.events().list(
       calendarId=calID, timeMin=now,
       maxResults=10, singleEvents=True,
       orderBy='startTime').execute()
   events = events_result.get('items', [])

   if not events:
       print('No upcoming events found.')
   for event in events:
       start = event['start'].get('dateTime', event['start'].get('date'))
       print(start, event['description'])

if __name__ == '__main__':
   main()