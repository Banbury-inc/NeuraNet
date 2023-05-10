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
from transformers import pipeline, T5Tokenizer, T5ForConditionalGeneration, GPT2LMHeadModel, AutoTokenizer, AutoModelForCausalLM, GPT2Tokenizer, LineByLineTextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments


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
    
    # Load the pre-trained GPT-2 model and tokenizer
    tokenizer = T5Tokenizer.from_pretrained('t5-base', model_max_length=1024)
    model = T5ForConditionalGeneration.from_pretrained('t5-base')

    # Create the pipeline
    text_classification_pipeline = pipeline('text-classification', model='distilbert-base-uncased-finetuned-sst-2-english')
    ner_pipeline = pipeline('ner', model='dslim/bert-base-NER')
    sentiment_analysis_pipeline = pipeline('sentiment-analysis', model='nlptown/bert-base-multilingual-uncased-sentiment')
    qa_pipeline = pipeline('question-answering', model='distilbert-base-cased-distilled-squad')
    

    # Set model to evaluation mode
    model.eval


    return model, tokenizer, text_classification_pipeline, ner_pipeline, sentiment_analysis_pipeline, qa_pipeline


def render_response(prompt, model, tokenizer, text_classification_pipeline, ner_pipeline, sentiment_analysis_pipeline, qa_pipeline):
    # Generate text
    
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    output = model.generate(input_ids=input_ids, max_length=500, num_beams=10, no_repeat_ngram_size=2, early_stopping=False, pad_token_id=tokenizer.eos_token_id, attention_mask=torch.ones(input_ids.shape))
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    

    # Use the pipeline to get the output from each model
    output1 = text_classification_pipeline(prompt)
    output2 = ner_pipeline(prompt)
    output3 = sentiment_analysis_pipeline(prompt)
    output4 = qa_pipeline({'question': 'What did the cat do?', 'context': prompt})


    response = [generated_text, output1, output2, output3, output4]

    return response


def main():
    # Start a conversation with the user
    prompt = start_conversation()

    # Load the pre-trained model and tokenizer
    model, tokenizer, text_classification_pipeline, ner_pipeline, sentiment_analysis_pipeline, qa_pipeline = load_model()

    # Continue the conversation until the user ends it
    while True:
        if prompt == "go to exploration mode":
            subprocess.run(['python', 'Artificial_Intelligence\exploration_mode.py'])
        else:
            response = render_response(prompt, model, tokenizer, text_classification_pipeline, ner_pipeline, sentiment_analysis_pipeline, qa_pipeline)
            print(response[0])
            print(response[1])
            print(response[2])
            print(response[3])
            print(response[4])
            
            prompt = continue_conversation()


if __name__ == "__main__":
    main()
