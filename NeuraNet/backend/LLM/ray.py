
import ray
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

@ray.remote
class InferenceWorker:
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model.to(torch.device("cpu"))  # Change to "cuda" if GPU is available

    def generate(self, input_ids, attention_mask):
        with torch.no_grad():
            outputs = self.model.generate(input_ids=input_ids, attention_mask=attention_mask, max_length=50)
        return outputs

def setup_workers(model_name, num_workers):
    workers = [InferenceWorker.remote(model_name) for _ in range(num_workers)]
    return workers

def distribute_inference(workers, text):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    inputs = tokenizer(text, return_tensors="pt")

    input_ids = inputs["input_ids"].split(len(workers), dim=1)
    attention_mask = inputs["attention_mask"].split(len(workers), dim=1)

    # Send input data to each worker
    futures = [worker.generate.remote(input_id, att_mask) for worker, input_id, att_mask in zip(workers, input_ids, attention_mask)]
    results = ray.get(futures)

    # Concatenate results from all workers
    generated_ids = torch.cat(results, dim=1)
    generated_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

    return generated_text

if __name__ == "__main__":
    ray.init(address='auto')

    model_name = "meta-llama/Meta-Llama-3-8B"
    num_workers = 2  # Adjust based on the number of available devices

    workers = setup_workers(model_name, num_workers)
    
    text = "Hey, how are you doing today?"
    generated_text = distribute_inference(workers, text)
    
    print(generated_text)
