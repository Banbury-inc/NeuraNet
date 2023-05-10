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
import ipfshttpclient
from transformers import GPT2Model, GPT2LMHeadModel, GPT2Tokenizer, LineByLineTextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments


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
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

    # Set model to evaluation mode
    model.eval


    return model, tokenizer


def render_response(prompt, model, tokenizer):
    # Generate text
    
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    output = model.generate(input_ids=input_ids, max_length=50, num_beams=5, no_repeat_ngram_size=2, early_stopping=True, pad_token_id=tokenizer.eos_token_id, attention_mask=torch.ones(input_ids.shape))
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    print(generated_text)
    response = generated_text

    return response


def main():
    # Start a conversation with the user
    prompt = start_conversation()

    # Load the pre-trained model and tokenizer
    model, tokenizer = load_model()

    # Continue the conversation until the user ends it
    while True:
        response = render_response(prompt, model, tokenizer)
        print(response)
        prompt = continue_conversation()


if __name__ == "__main__":
    main()
