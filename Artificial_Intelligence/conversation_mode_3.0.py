import numpy as np
import tensorflow as tf
import os
import sys
import math
from tensorflow.keras.layers import TextVectorization
import subprocess
from tqdm import tqdm
import transformers
import openai
import logging
import datetime
from transformers import pipeline, BertConfig, XLMRobertaForSequenceClassification, XLMRobertaTokenizer,  BertLMHeadModel, AutoModelForCausalLM, BertForSequenceClassification, BertTokenizer, BertModel, T5Tokenizer, T5ForConditionalGeneration, GPT2LMHeadModel, AutoTokenizer, AutoModelForCausalLM, GPT2Tokenizer, LineByLineTextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def start_conversation():
    print("Athena Version 0.0.1")
    print("Copyright 2023 Banbury Enterprises")
    print("All Rights Reserved")
    print(" ")
    prompt = input("-----> ")


    return prompt


def continue_conversation():
    prompt = input("-----> ")


    return prompt


def load_model():
    
    # Set up the OpenAI API credentials
    openai.api_key = "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"





def render_response(prompt):
    
    categories = ['summarization', 'coding', 'conversational', 'translation', 'question-answering', 'task-completion', 'add', 'show']
    # Call the OpenAI API to classify the sentence into one of the categories
    results = openai.Completion.create(
        engine= "text-davinci-003",
        prompt=f"Classify the following sentence into one of the given categories: \"{prompt}\". Categories: {categories}.",
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.0,
    )
    # Extract the predicted labels from the response
    label = str(results.choices[0].text.strip())
    
    return label
def calendar(prompt):
    print("Initiating calendar module")

    
    # Define the model to use for classification
    model = "text-davinci-003"

    # Define the list of categories to choose from
    categories = ['title', 'date', 'time']

    # Call the OpenAI API to classify the sentence into one of the categories
    response = openai.Completion.create(
        engine=model,
        prompt=f"Extract the following categories in the given sentence: \"{prompt}\". Categories: {categories}.",
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.0,
    )

    print(response)
    # Extract the predicted labels from the response
    outputs = response.choices[0].text.split("\n")
    print(outputs)

    # Initialize variables for title, time, and date
    title = ""
    time = ""
    date = ""


    for output in outputs:
        if output:
            label, value = output.split(":", 1)
            value = value.strip()
            if label.strip() == "Title":
                title = value
            elif label.strip() == "Time":
                time = value
            elif label.strip() == "Date":
                date = value
    print(title, time, date)

        
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
            'summary': title,
            'location': 'New York',
            'description': 'A test event for the Google Calendar API',
            'start': {
                'dateTime': date+'T'+time+'-04:00', # Change the date and time as per your needs
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
def calendar_remove_last_event(prompt):
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
        print('Getting the upcoming events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                                maxResults=10, singleEvents=True,
                                                orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Print the start and name of the last event
        last_event = events[-1]
        print(f"Removing event: {last_event['summary']}")
        service.events().delete(calendarId='primary', eventId=last_event['id']).execute()
        print('Event removed.')

    except HttpError as error:
        print('An error occurred: %s' % error)
def calender_recent_events(prompt):
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
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
def weather(prompt):
    print("Initiating weather module")
def maps(prompt):
    print("Initiating maps module")
def twitter(prompt):
    print("Initiating twitter module")
def spotify(prompt):
    print("Initiating spotify module")
def google_search(prompt):
    print("Initiating google search module")
def summarization(prompt):
    print("Initiating summarization module")
def coding(prompt):
    print("Initiating coding module")
    # organize tasks into functions
    # Define the model to use for code generation
    model = "text-davinci-002"

    # Call the OpenAI API to generate code based on the prompt
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extract the generated code from the response
    code = response.choices[0].text.strip()

    # Print the generated code
    print(code)
def conversational(prompt):
    print("Initiating conversational module")
def translation(prompt):
    print("Initiating translation module")
def question_answering(prompt):
    print("Initiating question-answering module")
def task_completion(prompt):
    print("Initiating task-completion module")

    sentence = prompt

    # Define the model to use for classification
    model = "text-davinci-003"

    # Define the list of categories to choose from
    categories = ['calendar', 'weather', 'maps', 'twitter', 'spotify', 'google search']

    # Call the OpenAI API to classify the sentence into one of the categories
    response = openai.Completion.create(
        engine=model,
        prompt=f"Classify the following sentence into one of the given categories: \"{sentence}\". Categories: {categories}.",
        max_tokens=20,
        n=1,
        stop=None,
        temperature=0.0,
    )

    label = response.choices[0].text.strip()
    response = label 
    print (response)
    if response == "Calendar":
        print("This prompt is most likely about something related to a calendar")
        # Define the model to use for classification
        model = "text-davinci-003"

        # Define the list of categories to choose from
        categories = ['add', 'delete', 'update', 'view']

        # Call the OpenAI API to classify the sentence into one of the categories
        response = openai.Completion.create(
            engine=model,
            prompt=f"Classify the following sentence into one of the given categories: \"{sentence}\". Categories: {categories}.",
            max_tokens=20,
            n=1,
            stop=None,
            temperature=0.0,
        )

        label = response.choices[0].text.strip()
        response = label 
        print (response)
        if response == "Add":
            print("This prompt is most likely about adding something to the calendar")
            calendar(prompt)
        elif response == "delete":
            print("This prompt is most likely about deleting something from the calendar")
            calendar_remove_last_event(prompt)
        elif response == "update":
            calendar(prompt)
            print("This prompt is most likely about updating something from the calendar")
        elif response == "view":
            print("This prompt is most likely about viewing something on the calendar")
            calender_recent_events(prompt)
    elif response == "weather":
        print("This prompt is most likely about weather")
        weather(prompt)
    elif response == "maps":
        print("This prompt is most likely about maps")
        maps(prompt)
    elif response == "twitter":
        print("This prompt is most likely about twitter")
        twitter(prompt)
    elif response == "spotify":
        print("This prompt is most likely about spotify")
        spotify(prompt)
    elif response == "google search":
        print("This prompt is most likely about google search")
        google_search(prompt)
def main():
    logging.disable(logging.CRITICAL)
    # Set up the OpenAI API credentials
    openai.api_key = "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"
    # Start a conversation with the user
    prompt = start_conversation()



    # Continue the conversation until the user ends it
    while True:
        if prompt == "go to exploration mode":
            subprocess.run(['python', 'Artificial_Intelligence\exploration_mode.py'])
        else:
            response = render_response(prompt)
            print("This prompt is most likely about " + response)
            if response == "summarization":
                summarization(prompt)
            elif response == "Coding":
                coding(prompt)
            elif response == "conversational":
                conversational(prompt)
            elif response == "translation":
                translation(prompt)
            elif response == "question-answering":
                question_answering(prompt)
            elif response == "Task-Completion":
                task_completion(prompt)
        prompt = continue_conversation()


if __name__ == "__main__":
    main()
