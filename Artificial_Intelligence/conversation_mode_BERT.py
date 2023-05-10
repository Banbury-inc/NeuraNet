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
import logging
import ipfshttpclient
from transformers import pipeline, BertConfig, BertLMHeadModel, AutoModelForCausalLM, BertForSequenceClassification, BertTokenizer, BertModel, T5Tokenizer, T5ForConditionalGeneration, GPT2LMHeadModel, AutoTokenizer, AutoModelForCausalLM, GPT2Tokenizer, LineByLineTextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments


def start_conversation():
    print("Athena Version 0.0.1")
    print("Copyright 2023 Banbury Enterprises")
    print("All Rights Reserved")
    print(" ")
    prompt = input("How may I help you?: ")
    return prompt


def continue_conversation():
    prompt = input("How may I help you?: ")
    return prompt


def load_model():
    
    # Load the pre-trained BERT model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained("PygmalionAI/pygmalion-6b")
    model = AutoModelForCausalLM.from_pretrained("PygmalionAI/pygmalion-6b")

    # load the default text classification pipeline
    text_classifier = pipeline("text-classification")

    # add BART-large-mnli model to the pipeline
    text_classifier.model.config.model_name_or_path = "facebook/bart-large-mnli"
    text_classifier.model = text_classifier.model.from_pretrained(
    text_classifier.model.config.model_name_or_path
    )
    

    # Set model to evaluation mode
    model.eval


    return model, tokenizer, text_classifier


def render_response(prompt, model, tokenizer, text_classifier):

    sequence_to_classify = prompt
    candidate_labels = ['summarization', 'coding', 'conversational', 'translation', 'question-answering']
    text_classifier(sequence_to_classify, candidate_labels)
    # Generate text
    encoded_input = tokenizer(prompt, return_tensors='pt')
    response_array = model(**encoded_input)
    response = tokenizer.decode(response_array[0], skip_special_tokens=True)
    return response


def main():
    # Start a conversation with the user
    prompt = start_conversation()

    # Load the pre-trained model and tokenizer
    model, tokenizer, text_classifier = load_model()

    # Continue the conversation until the user ends it
    while True:
        if prompt == "go to exploration mode":
            subprocess.run(['python', 'Artificial_Intelligence\exploration_mode.py'])
        else:
            response = render_response(prompt, model, tokenizer, text_classifier)
            print(response)
            
            prompt = continue_conversation()


if __name__ == "__main__":
    main()
