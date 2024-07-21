import json
import requests
import termcolor
import re
import argparse
from config import Config 

'''
Property of Banbury Innovations. All rights reserved.
Author: Michael Mills

This is Ollama with two agents talking to each other. Addding visuals so you can tell who is talking. 
'''


class GeneralAgent:

    def chat(self, messages):
        model = "llama3" 
        title = termcolor.colored("General Agent: ", "green")
        r = requests.post(
            "http://0.0.0.0:11434/api/chat",
            json={"model": model, "messages": messages, "stream": True, "options": {"num_predict": Config.max_tokens}},
            stream=True

        )
        r.raise_for_status()
        output = ""

        if Config.show_agent_dialogue == True:
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
                if Config.show_agent_dialogue == True:
                    print(content, end="", flush=True)

            if body.get("done", False):
                message["content"] = output
                return message

class CriticAgent:

    def chat(self, messages):
        model = "llama3" 
        title = termcolor.colored("Critic Agent: ", "yellow")
        role = "You are a critic agent. Your responsibilllity is to take the following response and give a rating between 0-10 of how good you think the response is. You are also to provide feedback on why you gave that rating"
        messages.insert(0, {"role": "system", "content": role})
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
    def parse_rating(self, response_text):
        # Extract the rating from the response text
        match = re.search(r'\b(\d+)\b', response_text)
        if match:
            rating = int(match.group(1))
            if 0 <= rating <= 10:
                return rating
        return None




class TaskManagementAgent:

    def chat(self, messages):
        model = "llama3" 
        title = termcolor.colored("Task Management Agent: ", "yellow")
        role = "You are a task management agent. Your responsibilllity is to take the following task and break it down into a list of subtasks."
        messages.insert(0, {"role": "system", "content": role})
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

def run_as_function(user_input):
    general_agent_messages = []
 
    general_agent_messages.append({"role": "user", "content": user_input})
    general_agent = GeneralAgent()
    general_agent_message  = general_agent.chat(general_agent_messages)
    general_agent_messages.append(general_agent_message)
    return general_agent_message["content"]


def main():
    general_agent_messages = []
    task_management_agent_messages = []
    critic_agent_messages = []
    critic_rating = 0
    loop = True
    
    while loop == True:
        if Config.prompt_as_command_line_argument == True:
            # Create the parser
            parser = argparse.ArgumentParser(description='Ollama with two agents talking to each other')
            parser.add_argument('prompt', type=str, help='The prompt to start the conversation')
            args = parser.parse_args()
            user_input = args.prompt
            loop = False
        else:
            user_input = input("Enter a prompt: ")
        if not user_input:
            exit()
        print()

        general_agent_messages.append({"role": "user", "content": user_input})
        general_agent = GeneralAgent()
        general_agent_message  = general_agent.chat(general_agent_messages)
        general_agent_messages.append(general_agent_message)
        print("\n\n")

        general_agent_message_content = general_agent_message["content"]


        while critic_rating <= Config.critic_rating_threshold:
            if Config.use_critic_agent == True:
                critic_agent_messages.append({"role": "user", "content": general_agent_message_content})
                critic_agent = CriticAgent()
                critic_agent_message  = critic_agent.chat(critic_agent_messages)
                critic_agent_messages.append(critic_agent_message)
                print("\n\n")
                #Parse the rating from the response text
                critic_rating = critic_agent.parse_rating(critic_agent_message["content"])
                if critic_rating is not None:
                    print(f"Rating: {critic_rating}")
                    print("\n\n")
                else:
                    print("Rating could not be parsed")
                    print("\n\n")
            else:
                critic_rating = 10

            if Config.use_task_management_agent == True:
                task_management_agent_messages.append({"role": "user", "content": user_input})
                task_management_agent = TaskManagementAgent()
                task_management_agent_message  = task_management_agent.chat(task_management_agent_messages)
                task_management_agent_messages.append(task_management_agent_message)
                print("\n\n")

            
            if Config.use_critic_agent == True:
                general_agent_messages.append({"role": "user", "content": critic_agent_message["content"]}) 
                general_agent_message  = general_agent.chat(general_agent_messages)
                general_agent_messages.append(general_agent_message)
                print("\n\n")

                general_agent_message_content = general_agent_message["content"]
        if Config.prompt_as_command_line_argument == True:
            return general_agent_message_content



if __name__ == "__main__":
    main()
