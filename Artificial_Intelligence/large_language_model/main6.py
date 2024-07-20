import json
import requests

'''
Property of Banbury Innovations. All rights reserved.
Author: Michael Mills

This is Ollama with two agents talking to each other.
'''


class GeneralAgent:

    def chat(self, messages):
        model = "llama3" 
        r = requests.post(
            "http://0.0.0.0:11434/api/chat",
            json={"model": model, "messages": messages, "stream": True},
        stream=True
        )
        r.raise_for_status()
        output = ""

        for line in r.iter_lines():
            body = json.loads(line)
            if "error" in body:
                raise Exception(body["error"])
            if body.get("done") is False:
                message = body.get("message", "")
                content = message.get("content", "")
                output += content
                # the response streams one token at a time, print that as we receive it
                print(content, end="", flush=True)

            if body.get("done", False):
                message["content"] = output
                return message


def main():
    messages1 = []
    messages2 = []

    user_input = input("Enter a prompt: ")
    while True:
        if not user_input:
            exit()
        print()
        messages1.append({"role": "user", "content": user_input})

        general_agent = GeneralAgent()
        message1  = general_agent.chat(messages1)
        messages1.append(message1)
        print("\n\n")

        user_input = message1["content"]



        messages2.append({"role": "user", "content": user_input})

        general_agent = GeneralAgent()
        message2  = general_agent.chat(messages2)
        messages1.append(message1)
        print("\n\n")

        user_input = message2["content"]





if __name__ == "__main__":
    main()
