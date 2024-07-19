import transformers
import torch



def initialize():
    model_id = "meta-llama/Meta-Llama-3-8B-instruct"

    pipeline = transformers.pipeline(
        "text-generation",
        model=model_id,
        model_kwargs={"torch_dtype": torch.bfloat16},
        device_map="auto",
        # device_map="cpu",
    )

    terminators = [
        pipeline.tokenizer.eos_token_id,
        pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    return pipeline, terminators

def generate_response(prompt, pipeline, terminators):
    messages = [
        # {"role": "system", "content": "You are a general agent. Your primary goal is to answer the following prompt using your llama3 model."},
        {"role": "user", "content": prompt},
    ]
    outputs = pipeline(
        messages,
        max_new_tokens=256,
        pad_token_id=terminators.pop(0),
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.6,
        top_p=0.9,
    )

    response = outputs[0]["generated_text"][-1]['content']
    return response


   

def main():
    pipeline, terminators = initialize()
    while True:
        try:
            prompt = input("Enter a prompt: ")
            response = generate_response(prompt, pipeline, terminators)
            print(response)
        except KeyboardInterrupt:
            break
if __name__ == "__main__":
    main()
