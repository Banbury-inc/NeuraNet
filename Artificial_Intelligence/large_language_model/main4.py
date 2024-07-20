'''
Property of Banbury Innovations. All rights reserved.
Author: Michael Mills

This code is essentially two master agents talking to each other. Memory issues when running on GPU. 

'''


import transformers
import torch
import gc



def initialize():
    model_id = "meta-llama/Meta-Llama-3-8B-instruct"

    pipeline = transformers.pipeline(
        "text-generation",
        model=model_id,
        # model_kwargs={"torch_dtype": torch.bfloat16},
        model_kwargs={"torch_dtype": torch.float16},
        # device_map="auto",
        device_map="cpu",
    )

    terminators = [
        pipeline.tokenizer.eos_token_id,
        pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        # pipeline.tokenizer.convert_tokens_to_ids("")
    ]

    eos_token_id = pipeline.tokenizer.eos_token_id
    

    return pipeline, terminators, eos_token_id

class MasterAgent:
    def generate(self, prompt, pipeline, terminators, eos_token_id):
        messages = [
            # {"role": "system", "content": "You are a general agent. Your primary goal is to answer the following prompt using your llama3 model."},
            {"role": "user", "content": prompt},
        ]
        outputs = pipeline(
            messages,
            max_new_tokens=10,
            # pad_token_id=terminators.pop(0),
            pad_token_id=eos_token_id,
            eos_token_id=eos_token_id,
            batch_size=1,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
        )

        response = outputs[0]["generated_text"][-1]['content']
        return response

class CriticAgent:
    def generate(self, prompt, pipeline, terminators):

        role = '''
        You are a critic agent. You are to determine how well the client's question has been
        answered. Your role is to give a rating from 1 to 10, 1 being incomplete 
        and 10 being complete. You are to provide the rating from 1 to 10 and an explanation
        as to why you gave it that rating.
        '''

        messages = [
            {"role": "system", "content": role},
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
    pipeline, terminators, eos_token_id = initialize()
    master_agent = MasterAgent()
    critic_agent = CriticAgent()
    while True:
        try:
            prompt = input("Enter a prompt: ")
            master_agent_response = master_agent.generate(prompt, pipeline, terminators, eos_token_id)
            print(master_agent_response)
            del prompt
            torch.cuda.empty_cache()
            gc.collect()
            while True:
                master_agent_response = master_agent.generate(master_agent_response, pipeline, terminators, eos_token_id)
                print(master_agent_response)
                torch.cuda.empty_cache()
                gc.collect()
        except KeyboardInterrupt:
            break



if __name__ == "__main__":
    main()

