import json
import requests
import termcolor

'''
Property of Banbury Innovations. All rights reserved.
Author: Michael Mills

This is Ollama with two agents talking to each other. Addding visuals so you can tell who is talking. 
'''


class GeneralAgent:

    def chat(self, messages):
        model = "llama3" 
        title = termcolor.colored("General Agent 1: ", "green")
        r = requests.post(
            "http://0.0.0.0:11434/api/chat",
            json={"model": model, "messages": messages, "stream": True},
        stream=True
        )
        r.raise_for_status()
        output = ""

        print(title)
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

class GeneralAgent2:

    def chat(self, messages):
        model = "llama3" 
        title = termcolor.colored("General Agent 2: ", "red")
        r = requests.post(
            "http://0.0.0.0:11434/api/chat",
            json={"model": model, "messages": messages, "stream": True},
        stream=True
        )
        r.raise_for_status()
        output = ""
        print(title)
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

class CriticAgent:

    def chat(self, messages):
        model = "llama3" 
        title = termcolor.colored("Critic Agent: ", "blue")
        r = requests.post(
            "http://0.0.0.0:11434/api/chat",
            json={"model": model, "messages": messages, "stream": True},
        stream=True
        )
        r.raise_for_status()
        output = ""
        print(title)
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

class TaskManagementAgent:

    def chat(self, messages):
        model = "llama3" 
        title = termcolor.colored("Task Management Agent: ", "yellow")
        r = requests.post(
            "http://0.0.0.0:11434/api/chat",
            json={"model": model, "messages": messages, "stream": True},
        stream=True
        )
        r.raise_for_status()
        output = ""
        print(title)
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
    task_management_agent_messages = []
    critic_agent_messages = []

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

        general_agent = GeneralAgent2()
        message2  = general_agent.chat(messages2)
        messages1.append(message1)
        print("\n\n")

        user_input = message2["content"]





if __name__ == "__main__":
    main()
