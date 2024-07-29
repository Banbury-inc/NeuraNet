# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")

messages = [
    {"role": "user", "content": "Who are you?"},
]

# Tokenize input
input_ids = tokenizer(messages[0]["content"], return_tensors="pt").input_ids

# Generate text
output = model.generate(input_ids, max_length=50)

# Decode output
decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)

print(decoded_output)
