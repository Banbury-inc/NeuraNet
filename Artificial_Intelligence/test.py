import requests
import json
import os
import pandas as pd
import tensorflow as tf
import subprocess
import json
import platform
import time
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import ipfshttpclient
from flair.data import Sentence
from flair.models import SequenceTagger
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, time, timedelta
import pytz
import google.auth



import datetime
import os.path
from google.cloud import language_v1
from google.cloud.language_v1 import Document, LanguageServiceClient
from google.cloud.language_v1.types import Document, EncodingType
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dateutil import parser
from dateutil.parser import parse
from allennlp.predictors import Predictor

def recent_events():
        # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/calendar']
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'C:\\Users\\mmill\\OneDrive\\Documents\\API Keys\\credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('calendar', 'v3', credentials=creds)

            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            print('Getting the upcoming 10 events')
            events_result = service.events().list(calendarId='primary', timeMin=now,
                                                maxResults=10, singleEvents=True,
                                                orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
                return

            # Prints the start and name of the next 10 events
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])

        except HttpError as error:
            print('An error occurred: %s' % error)    

def add_event():
    # If modifying these scopes, delete the file token.json.
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/calendar']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'C:\\Users\\mmill\\OneDrive\\Documents\\API Keys\\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Adding an event to the calendar')
        event = {
            'summary': 'Test Event',
            'location': 'New York',
            'description': 'A test event for the Google Calendar API',
            'start': {
                'dateTime': '2023-05-12T10:00:00-04:00', # Change the date and time as per your needs
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': '2023-05-12T11:00:00-04:00', # Change the date and time as per your needs
                'timeZone': 'America/New_York',
            },
            'reminders': {
                'useDefault': True,
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f'Event created: {event.get("htmlLink")}')

    except HttpError as error:
        print('An error occurred: %s' % error)

def date_time_natural_language_extraction():
    # Load the AllenNLP predictor
    predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/fine-grained-ner.2021-08-27.tar.gz")

    # Define the string to parse
    text = "I will arrive on May 14th at 2pm"

    # Use the predictor to extract the date and time
    result = predictor.predict(sentence=text)

    # Extract the relevant parts of the result
    date = result["spans"][0]["text"]
    time = result["spans"][1]["text"]

    # Convert the date and time into a datetime object
    date_obj = datetime.datetime.strptime(f'{date} {time}', '%B %d %Y %I:%M%p')

    # Print the datetime object
    print(date_obj)
def main():
    date_time_natural_language_extraction()
if __name__ == '__main__':
    main()
