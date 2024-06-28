import torch
import transformers
import time

start_time = time.time()
model_id = "meta-llama/Meta-Llama-3-8B"
max_tokens = 20

pipeline = transformers.pipeline(
    "text-generation", model=model_id, pad_token_id=50256, model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto"
)


response = pipeline("Hey how are you doing today?", 
                    max_new_tokens=max_tokens, 
                    truncation=True)
end_time = time.time()
print(response)
print(f"Time taken: {end_time - start_time} seconds")
print(f"Time taken: {end_time - start_time} seconds")



