
from transformers import AutoTokenizer
from petals import AutoDistributedModelForCausalLM

INITIAL_PEERS = ["/ip4/10.123.1.93/tcp/44903/p2p/QmNR1bpUDiHvpfLYYT5XSiuvT4xw7WQZFViUtgtBj7fZEw"]
# Choose any model available at https://health.petals.dev
# model_name = "meta-llama/Meta-Llama-3-8B-instruct"
model_name = "meta-llama/Meta-Llama-3-8B-instruct"

# Total of 31 blocks

# Connect to a distributed network hosting model layers
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoDistributedModelForCausalLM.from_pretrained(model_name, initial_peers=INITIAL_PEERS)

# Function to generate inference
def generate_inference(prompt, max_new_tokens=50):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=max_new_tokens)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text
prompt = "Once upon a time"
generated_text = generate_inference(prompt)
print(f"Generated Text: {generated_text}")
