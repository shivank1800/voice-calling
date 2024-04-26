import speech_recognition as sr
import os
from gtts import gTTS
import pyttsx3
recognizer = sr.Recognizer()
import re
from datetime import datetime
import pytz
from create_event import create_event
def format_time(input_time):
    time = input_time.split(" to ")
    s = datetime.strptime(time[0].replace('.', ''), '%I:%M %p')
    e = datetime.strptime(time[1].replace('.', ''), '%I:%M %p')
    # Format the datetime object into a 24-hour time string
    sd =s.strftime('%H:%M')
    ed = e.strftime('%H:%M')
    return sd,ed


def convert_date_format(input_date):
    months = {
        'january': '01',
        'february': '02',
        'march': '03',
        'april': '04',
        'may': '05',
        'june': '06',
        'july': '07',
        'august': '08',
        'september': '09',
        'october': '10',
        'november': '11',
        'december': '12'
    }
    
    # Regular expression to match various date formats
    date_regex = r'(\d{1,2})(st|nd|rd|th)?[ -/]?(\d{1,2}|[a-zA-Z]+)[ -/]?(\d{4})'
    match = re.search(date_regex, input_date.lower())
    
    if match:
        day, _, month, year = match.groups()
        
        if month.isdigit():
            month = month.zfill(2)
        else:
            month = months.get(month.lower())
            
        formatted_date = f"{year}-{month}-{day}"
        print(formatted_date)
        try:
            datetime.strptime(formatted_date, '%Y-%m-%d')
            return formatted_date
        except ValueError:
            return None
    else:
        return None

def listen_date(source):
    try:
        recorded_audio = recognizer.listen(source, timeout=4)
        print("Done recording.")
        print("Recognizing the text...")
        text = recognizer.recognize_google(recorded_audio, language="en-US")
        print("Decoded Text: {}".format(text))
        # date_object = datetime.strptime(text, "%dth %B %Y")
        # formatted_date = date_object.strftime("%Y-%m-%d")
        formatted_date = convert_date_format(text)
        if not formatted_date:
            engine = pyttsx3.init()
            engine.setProperty("rate", 178)
            engine.say("could not understand date, please speak again")
            engine.runAndWait()
        print(formatted_date)
        engine = pyttsx3.init()
        engine.setProperty("rate", 178)
        engine.say(formatted_date)
        engine.runAndWait()
        return formatted_date
    except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
    except Exception as ex:
        print("Error during recognition:", ex)


def listen_time(source):
    try:
        recorded_audio = recognizer.listen(source, timeout=4)
        print("Done recording.")
        print("Recognizing the text...")
        text = recognizer.recognize_google(recorded_audio, language="en-US")
        print("Decoded Text: {}".format(text))
        format_time(text)
        starttime,endtime = format_time(text)
        print(starttime,endtime)
        engine = pyttsx3.init()
        engine.setProperty("rate", 178)
        engine.say(text)
        engine.runAndWait() 
        return starttime,endtime
    except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
    except Exception as ex:
        print("Error during recognition:", ex)

def main():
    try:
        # List available microphones (optional)
        print("Available microphones:")
        print(sr.Microphone.list_microphone_names())
        with sr.Microphone() as source:
            print("Adjusting noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Recording for 4 seconds...")
            date = listen_date(source)
            st,et = listen_time(source)
            print(date+"T"+st+":00+05:30")
            create_event(date+"T"+st+":00+05:30",date+"T"+et+":00+05:30")
    except Exception as e:
        print(e)

main()