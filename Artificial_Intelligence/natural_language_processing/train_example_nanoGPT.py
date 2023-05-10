import numpy as np
import tensorflow_datasets as tfds
import tensorflow as tf
tfds.disable_progress_bar()
import matplotlib.pyplot as plt
import os
import sys
import math
sys.path.append('"E:\Datasets\openwebtext"')
from tensorflow.keras.layers import TextVectorization
import subprocess
# from tensorflow.contrib.training import HParams
from tqdm import tqdm
import tiktoken
from datasets import load_dataset # huggingface datasets
import torch
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.distributed import init_process_group, destroy_process_group

import dill as pickle
import dill
from contextlib import nullcontext
from transformers import GPT2LMHeadModel
import torch.nn as nn
from torch.nn import functional as F
from dataclasses import dataclass
import tokenizers as tk
from transformers import GPT2LMHeadModel, AutoModelForCausalLM, GPT2Tokenizer, LineByLineTextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments


# saves the openwebtext dataset to a binary file for training. following was helpful:
# https://github.com/HazyResearch/flash-attention/blob/main/training/src/datamodules/language_modeling_hf.py


def process_dataset():
    # number of workers in .map() call
    # good number to use is ~order number of cpu cores // 2
    num_proc = 2

    # takes 54GB in huggingface .cache dir, about 8M documents (8,013,769)
    dataset = load_dataset("openwebtext")

    # owt by default only contains the 'train' split, so create a test split
    split_dataset = dataset["train"].train_test_split(test_size=0.0005, seed=2357, shuffle=True)
    split_dataset['val'] = split_dataset.pop('test') # rename the test split to val

    # this results in:
    # >>> split_dataset
    # DatasetDict({
    #     train: Dataset({
    #         features: ['text'],
    #         num_rows: 8009762
    #     })
    #     val: Dataset({
    #         features: ['text'],
    #         num_rows: 4007
    #     })
    # })

    # we now want to tokenize the dataset. first define the encoding function (gpt2 bpe)
    enc = tiktoken.get_encoding("gpt2")
    def process():
        def tokenize(batch):
            return enc.encode_batch(batch["text"])

        split_dataset = split_dataset.map(
            tokenize,
            batched=True,
            batch_size=1000,
            num_proc=num_proc,
            remove_columns=["text"],
            desc="Running tokenizer on dataset",
        )

        return split_dataset
  



    # tokenize the dataset
    tokenized = split_dataset.map(
        process,
        remove_columns=['text'],
        desc="tokenizing the splits",
        num_proc=num_proc,
    )

    # concatenate all the ids in each dataset into one large file we can use for training
    for split, dset in tokenized.items():
        arr_len = np.sum(dset['len'])
        filename = os.path.join(os.path.dirname(__file__), f'{split}.bin')
        dtype = np.uint16 # (can do since enc.max_token_value == 50256 is < 2**16)
        arr = np.memmap(filename, dtype=dtype, mode='w+', shape=(arr_len,))
        total_batches = 1024

        idx = 0
        for batch_idx in tqdm(range(total_batches), desc=f'writing {filename}'):
            # Batch together samples for faster write
            batch = dset.shard(num_shards=total_batches, index=batch_idx, contiguous=True).with_format('numpy')
            arr_batch = np.concatenate(batch['ids'])
            # Write into mmap
            arr[idx : idx + len(arr_batch)] = arr_batch
            idx += len(arr_batch)
        arr.flush()

    # train.bin is ~17GB, val.bin ~8.5MB
    # train has ~9B tokens (9,035,582,198)
    # val has ~4M tokens (4,434,897)

    # to read the bin files later, e.g. with numpy:
    # m = np.memmap('train.bin', dtype=np.uint16, mode='r')

def train_model():
    # Load the tokenizer and model
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    # Load the training data
    train_dataset = LineByLineTextDataset(
        tokenizer=tokenizer,
        file_path="train.bin",
        block_size=128,
    )

    # Load the validation data
    eval_dataset = LineByLineTextDataset(
        tokenizer=tokenizer,
        file_path="val.bin",
        block_size=128,
    )

    # Define the data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False,
    )

    # Define the training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="steps",
        eval_steps=500,
        save_total_limit=2,
        learning_rate=1e-4,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        num_train_epochs=1,
        logging_steps=500,
        save_steps=500,
    )

    # Define the Trainer and start training
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        data_collator=data_collator,
        eval_dataset=eval_dataset,
    )

    trainer.train()

    return trainer
def save_dataset(trainer):
    # create a counter to keep track of the number of datasets generated, and 
    # write the number of datasets to a file


    # determine the value of counter based on what the number is in Number_of_Datasets.txt

    with open("Artificial_Intelligence\\Number_of_Datasets.txt", "r") as f:
        counter = int(f.read())
        counter += 1
    with open("Artificial_Intelligence\\Number_of_Datasets.txt", "w") as f:
        #write the value of counter to the file
        f.write(str(counter))
        f.close()


    # specify the directory path to create
    directory = "E:\Models"+str(counter)

    # check if directory already exists
    if not os.path.exists(directory):
        # create directory
        os.makedirs(directory)
        print(f"Directory {directory} created successfully.")
    else:
        print(f"Directory {directory} already exists.")



        
    # generate a unique file name for the saved model
    model_name = f"model_{counter}.h5"
    file_path = f"E:\Models{model_name}"

    # save the model to the file path
    trainer.save_model(file_path)

    # Start a new IPFS daemon process using the 'ipfs daemon' command
    daemon_process = subprocess.Popen(["ipfs", "daemon"])

    # Wait for the daemon to start up (optional)

    # Upload the file using the 'ipfs add' command
    add_output = subprocess.check_output(["ipfs", "add", "-r", file_path])

    # Extract the hash of the uploaded file from the output
    file_hash = add_output.split()[1]

    # save the hash to CID's.txt file
    with open("Artificial_Intelligence\\CID's.txt", "a") as f:
        f.write(f"{model_name}: {file_hash.decode()}\n")

    # Print the hash to the console
    print(f"Uploaded file '{file_path}' to IPFS with hash '{file_hash.decode()}'")

    # Stop the IPFS daemon process
    daemon_process.terminate()


    with open("current_topic.txt", "r") as file:
        topic = file.read().strip()
    print(topic)
    # Open the file for appending and add the new topic
    with open("Artificial_Intelligence\\topics.txt", "a") as file:
        file.write(topic + "\n")

def main():
    process_dataset()
    trainer = train_model()
    save_dataset(trainer)

if __name__ == '__main__':
    main()