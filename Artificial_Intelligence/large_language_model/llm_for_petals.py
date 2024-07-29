import time
from transformers import AutoTokenizer
from petals import AutoDistributedModelForCausalLM

INITIAL_PEERS = [
    "/ip4/10.162.0.2/tcp/31337/p2p/QmWKMFsN5sfLSe2JXrCUpjUBuhHMbyGN2nfZbmHUH11VT7",
]

# Choose any model available at https://health.petals.dev
model_name = "stabilityai/StableBeluga-7B"  # This one is fine-tuned Llama 2 (70B)

# Connect to a distributed network hosting model layers
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoDistributedModelForCausalLM.from_pretrained(
    model_name, initial_peers=INITIAL_PEERS
)

# Run the model as if it were on your computer
inputs = tokenizer("What are your thoughts about Andre Agassi?", return_tensors="pt")["input_ids"]

starting_time = time.time()
outputs = model.generate(
    inputs,
    min_length=100,  # Ensure at least 100 tokens are generated
    max_new_tokens=100,  # Generate up to 100 tokens
    do_sample=True,  # Enable sampling to ensure diversity
    temperature=1.0,  # Control the randomness of predictions
    num_return_sequences=1  # Number of sequences to return
)
ending_time = time.time()

# Calculate the inference time and tokens per second
inference_time = ending_time - starting_time
tokens_generated = outputs.shape[1]  # Get the number of tokens generated
tokens_per_second = tokens_generated / inference_time

# Print results
print(f"Inference time: {inference_time:.2f} seconds")
print(f"Tokens generated: {tokens_generated}")
print(f"Tokens per second: {tokens_per_second:.2f}")
print(tokenizer.decode(outputs[0]))  # Decode and print the generated text

