import numpy as np
import tensorflow_datasets as tfds
import tensorflow as tf
tfds.disable_progress_bar()
import matplotlib.pyplot as plt
import os
import sys
import math
from tensorflow.keras.layers import TextVectorization
import subprocess
from tqdm import tqdm
import transformers
import torch
import data
import logging
import datetime
import ipfshttpclient
from transformers import pipeline, BertConfig, XLMRobertaForSequenceClassification, XLMRobertaTokenizer,  BertLMHeadModel, AutoModelForCausalLM, BertForSequenceClassification, BertTokenizer, BertModel, T5Tokenizer, T5ForConditionalGeneration, GPT2LMHeadModel, AutoTokenizer, AutoModelForCausalLM, GPT2Tokenizer, LineByLineTextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments
from flair.data import Sentence
from flair.models import SequenceTagger
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
    

    # load the default text classification pipeline
    text_classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")

    # add BART-large-mnli model to the pipeline
    text_classifier.model.config.model_name_or_path = "facebook/bart-large-mnli"
    text_classifier.model = text_classifier.model.from_pretrained(
    text_classifier.model.config.model_name_or_path
    )
    # Load the XLM-RoBERTa tokenizer
    tokenizer2 = XLMRobertaTokenizer.from_pretrained("xlm-roberta-base")

# Load the fine-tuned XLM-RoBERTa model
    model2 = XLMRobertaForSequenceClassification.from_pretrained("xlm-roberta-base")
    # Define the instruction detection pipeline
    instruction_detector = pipeline('fill-mask', model='xlm-roberta-base'
    )

    return text_classifier, instruction_detector, tokenizer2, model2


def render_response(prompt, text_classifier, instruction_detector, tokenizer2, model2):
    sequence_to_classify = prompt
    candidate_labels = ['summarization', 'coding', 'conversational', 'translation', 'question-answering', 'task-completion', 'add', 'show']
    results = text_classifier(sequence_to_classify, candidate_labels)
    max_score = 0
    max_label = None
    response = results['labels'][0]
            
   
    return response
def calendar(prompt, text_classifier, instruction_detector, tokenizer2, model2):
    print("Initiating calendar module")

    classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")

    sequence_to_classify = prompt
    words = sequence_to_classify.split()
    date_max_score = 0
    time_max_score = 0
    title_max_score = 0
    date_dict = {}
    time_dict = {}
    title_dict = {}
    date_candidate_labels = ['date']
    words = sequence_to_classify.split()
    for word in words:
        results = classifier(word, date_candidate_labels)
        score = results['scores'][0]
        date_dict[word] = score
    # sort the dictionary by values in descending order
    sorted_date_dict = dict(sorted(date_dict.items(), key=lambda item: item[1], reverse=True))
    #print the first value of the dictionary
    date_max_word = next(iter(sorted_date_dict))
    date_max_score = next(iter(sorted_date_dict.values()))
    date_second_max_word = list(sorted_date_dict)[1]

    date_candidate_labels = ['time']
    words = sequence_to_classify.split()
    for word in words:
        results = classifier(word, date_candidate_labels)
        score = results['scores'][0]
        time_dict[word] = score
    # sort the dictionary by values in descending order
    sorted_time_dict = dict(sorted(time_dict.items(), key=lambda item: item[1], reverse=True))
    #print the first value of the dictionary
    time_max_word = next(iter(sorted_time_dict))
    time_max_score = next(iter(sorted_time_dict.values()))
    time_second_max_word = list(sorted_time_dict)[1]
    date_candidate_labels = ['title']
    words = sequence_to_classify.split()
    for word in words:
        results = classifier(word, date_candidate_labels)
        score = results['scores'][0]
        title_dict[word] = score
    # sort the dictionary by values in descending order
    sorted_title_dict = dict(sorted(title_dict.items(), key=lambda item: item[1], reverse=True))
    #print the first value of the dictionary
    title_max_word = next(iter(sorted_title_dict))
    title_max_score = next(iter(sorted_title_dict.values()))
    title_second_max_word = list(sorted_title_dict)[1]
    if date_max_word == time_max_word:
        if date_max_score > time_max_score:
            time_max_word = time_second_max_word
        elif date_max_score < time_max_score:
            date_max_word = date_second_max_word
    if time_max_word == title_max_word:
        if time_max_score > title_max_score:
            title_max_word = title_second_max_word
        elif time_max_score < title_max_score:
            time_max_word = date_second_max_word
    if date_max_word == title_max_word:
        if date_max_score > time_max_score:
            time_max_word = time_second_max_word
        elif date_max_score < time_max_score:
            date_max_word = date_second_max_word
    print ("date: ", date_max_word, "time: ", time_max_word , "title: ", title_max_word)

        
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
            'summary': title_max_word,
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
def calendar_remove_last_event(prompt, text_classifier, instruction_detector, tokenizer2, model2):
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
def calender_recent_events(prompt, text_classifier, instruction_detector, tokenizer2, model2):
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
def weather(prompt, text_classifier, instruction_detector):
    print("Initiating weather module")
def maps(prompt, text_classifier, instruction_detector):
    print("Initiating maps module")
def twitter(prompt, text_classifier, instruction_detector):
    print("Initiating twitter module")
def spotify(prompt, text_classifier, instruction_detector):
    print("Initiating spotify module")
def google_search(prompt, text_classifier, instruction_detector):
    print("Initiating google search module")
def summarization(prompt, text_classifier, instruction_detector):
    print("Initiating summarization module")
def coding(prompt, text_classifier, instruction_detector):
    print("Initiating coding module")
def conversational(prompt, text_classifier, instruction_detector):
    print("Initiating conversational module")
def translation(prompt, text_classifier, instruction_detector):
    print("Initiating translation module")
def question_answering(prompt, text_classifier, instruction_detector):
    print("Initiating question-answering module")
def task_completion(prompt, text_classifier, instruction_detector, tokenizer2, model2):
    print("Initiating task-completion module")
    sequence_to_classify = prompt
    candidate_labels = ['calendar', 'weather', 'maps', 'twitter', 'spotify', 'google search']
    results = text_classifier(sequence_to_classify, candidate_labels)
    response = results['labels'][0]
    if response == "calendar":
        print("This prompt is most likely about something related to a calendar")
        sequence_to_classify = prompt
        candidate_labels = ['add', 'delete', 'update', 'view']
        results = text_classifier(sequence_to_classify, candidate_labels)
        response = results['labels'][0]
        if response == "add":
            print("This prompt is most likely about adding something to the calendar")
            calendar(prompt, text_classifier, instruction_detector, tokenizer2, model2)
        elif response == "delete":
            print("This prompt is most likely about deleting something from the calendar")
            calendar_remove_last_event(prompt, text_classifier, instruction_detector, tokenizer2, model2)
        elif response == "update":
            print("This prompt is most likely about updating something from the calendar")
        elif response == "view":
            print("This prompt is most likely about viewing something on the calendar")
            calender_recent_events(prompt, text_classifier, instruction_detector, tokenizer2, model2)
    elif response == "weather":
        print("This prompt is most likely about weather")
        weather(prompt, text_classifier, instruction_detector)
    elif response == "maps":
        print("This prompt is most likely about maps")
        maps(prompt, text_classifier, instruction_detector)
    elif response == "twitter":
        print("This prompt is most likely about twitter")
        twitter(prompt, text_classifier, instruction_detector)
    elif response == "spotify":
        print("This prompt is most likely about spotify")
        spotify(prompt, text_classifier, instruction_detector)
    elif response == "google search":
        print("This prompt is most likely about google search")
        google_search(prompt, text_classifier, instruction_detector)
def main():
    logging.disable(logging.CRITICAL)
    # Start a conversation with the user
    prompt = start_conversation()

    # Load the pre-trained model and tokenizer
    text_classifier, instruction_detector, tokenizer2, model2 = load_model()

    # Continue the conversation until the user ends it
    while True:
        if prompt == "go to exploration mode":
            subprocess.run(['python', 'Artificial_Intelligence\exploration_mode.py'])
        else:
            response = render_response(prompt, text_classifier, instruction_detector, tokenizer2, model2)
            print("This prompt is most likely about " + response)
            if response == "summarization":
                summarization(prompt, text_classifier, instruction_detector)
            elif response == "coding":
                coding(prompt, text_classifier, instruction_detector)
            elif response == "conversational":
                conversational(prompt, text_classifier, instruction_detector)
            elif response == "translation":
                translation(prompt, text_classifier, instruction_detector)
            elif response == "question-answering":
                question_answering(prompt, text_classifier, instruction_detector)
            elif response == "task-completion":
                task_completion(prompt, text_classifier, instruction_detector, tokenizer2, model2)
            elif response == "add":
                task_completion(prompt, text_classifier, instruction_detector, tokenizer2, model2)
            elif response == "show":
                task_completion(prompt, text_classifier, instruction_detector, tokenizer2, model2)
        prompt = continue_conversation()


if __name__ == "__main__":
    main()
