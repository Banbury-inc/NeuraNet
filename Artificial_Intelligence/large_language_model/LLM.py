from langchain.llms import Ollama
import re
from termcolor import colored
import queue
'''
AI Agents to Implement:

Task Management Agent:
- Queue system. Parse the list and make them individual objects that are placed in some type 
of list. 

Vision Agent:
- Detects objects in the environment and sends them as messages to other agents (e.g., a robot)
- captures image of the environment and generates description in words of what the environment
is like
- 
Health Agent:
- Monitors CPU, GPU, Memory and determines if the computer is in a good state. Sends messages to
task management agent if something needs to be turned off.

Motor Control Agent:
- Makes movements of motors, returns motor positions.

Navigation Agent:
- Able to take in cordinates, return coordinates
'''
class MasterAgent:
    def __init__(self):
        self.llm = Ollama(model="llama2")
        self.role = colored("Master Agent: ", "green", attrs=["bold"])
        self.responsibility = '''
        You are the master agent. Your role is to receive the request from the client,
        acknoledge that you have received the clients request and that you will begin working on it,
        determine which types of agents are needed in order to complete the task, and
        send back the response.

        '''
    def initialize():
        print("")
        prompt = input("--> ") 
        MasterAgent.communicate(prompt) 
    def communicate(prompt):
        master_agent = MasterAgent()
        response = master_agent.llm.predict(prompt)
        print("")
        print(master_agent.role + response)
        task_agent = TaskManagementAgent()
        task_agent.communicate(response)
    def recruit():
        # TODO: Analayze a list of all of the possible agents that can be recruited, 
        # determine which ones would be best to recruit, and recruit them.
        pass
class GeneralAgent:
    def __init__(self):
        self.llm = Ollama(model="llama2")
        self.role = colored("General Agent: ", "green", attrs=["bold"])
        self.responsibility = '''
        You are a general agent. Your primary goal is to answer the following prompt using your llama2 model

        '''
    def communicate(self, prompt):
        interpretation = self.responsibility + prompt 
        response = self.llm.predict(interpretation)
        print("")
        print(self.role + response)
        critic_agent = CriticAgent()
        evaluation, rating = critic_agent.evaluate(prompt)
        rating = int(rating)
        if rating < 8:
            self.revise(prompt, (evaluation, rating))
        else:
            if rating >= 8:
                MasterAgent.initialize()
    def revise(self, oldResponse, evaluation):
        evaluation_reasoning, rating = evaluation
        interpretation = self.responsibility + " The last response was " + oldResponse + "." + "The feedback about that response is the following: " + evaluation_reasoning + "Fix it." 
        response = self.llm.predict(interpretation)
        print("")
        print(self.role + response)
        critic_agent = CriticAgent()
        evaluation, rating = critic_agent.evaluate(self.role + response)
        rating = int(rating)
        if rating < 8: 
            evaluation, rating = critic_agent.evaluate(self.role + response)
            TaskManagementAgent.revise(self, oldResponse, evaluation)
        else:
            if rating >= 8:
                MasterAgent.initialize()
 


class TaskManagementAgent:
    def __init__(self):
        self.llm = Ollama(model="llama2")
        self.role = colored("Task Management Agent: ", "green", attrs=["bold"])
        self.responsibility = '''
        You are a task management agent. Your role is to give a numbered list of steps needed
        in order to accomplish the task, which is provided below. You are to return nothing 
        but a numbered list.

        '''
        self.tasks: list[str] = []
        self.revisions = 0 
        self.task = "This is the current task"
        # The number of revisions could potentially be a good idea to prevent loops. Maybe if the number of revisions is high enough, 
        # a different AI agent can be recruited to solve the problem. 
    def communicate(self, prompt):
        interpretation = self.responsibility + prompt 
        response = self.llm.predict(interpretation)
        print("")
        print(self.role + response)
        critic_agent = CriticAgent()
        evaluation, rating = critic_agent.evaluate(prompt)
        rating = int(rating)
        if rating < 8:
            self.revisions = self.revisions + 1
            self.revise(prompt, (evaluation, rating))
        else:
            if rating >= 8:
                MasterAgent.initialize()
    def revise(self, oldResponse, evaluation):
        evaluation_reasoning, rating = evaluation
        interpretation = self.responsibility + " The last response was " + oldResponse + "." + "The feedback about that response is the following: " + evaluation_reasoning + "Fix it." 
        response = self.llm.predict(interpretation)
        print("")
        print(self.role + response)
        critic_agent = CriticAgent()
        evaluation, rating = critic_agent.evaluate(self.role + response)
        rating = int(rating)
        if rating < 8: 
            evaluation, rating = critic_agent.evaluate(self.role + response)
            self.revisions = self.revisions + 1
            TaskManagementAgent.revise(self, oldResponse, evaluation)
        else:
            if rating >= 8:
                TaskManagementAgent.parse_and_process_plan()
    def plan(self, prompt):
        interpretation = self.responsibility + prompt 
        response = self.llm.predict(interpretation)
        print("")
        print(self.role + response)
        critic_agent = CriticAgent()
        evaluation, rating = critic_agent.evaluate(prompt)
        rating = int(rating)
        if rating < 8:
            self.revise(prompt, (evaluation, rating))
        else:
            if rating >= 8:
                tasks = TaskManagementAgent.parse_and_process_plan() # tasks is returned as a list of strings
                for task in tasks:
                    TaskManagementAgent.add_task(self, task)  
                    parsed_steps_string = '\n'.join(tasks)
                    print(parsed_steps_string)
                    TaskManagementAgent.execute()
    def execute(self, prompt):
        # TODO: create a function that will take the next task and refer it to the master agent.
        self.task = TaskManagementAgent.get_task(self)

        pass
    def parse_and_process_plan(self, prompt):
        # TODO: take the numbered list of actions needed to be taken in order to complete the task,
        # and add each task to a list.
        # Regular expression to split the string at each step
        # This pattern looks for digits followed by a period or parenthesis
        pattern = r'\d+\.\s*|\d+\)\s*'
        # Split the string using the regular expression
        tasks = re.split(pattern, prompt)
        # Remove any empty strings that may result from splitting
        tasks = [task.strip() for task in tasks if task.strip()]
        return tasks
    def add_task(self, task):
        """Adds a task to the queue."""
        try:
            self._tasks.put_nowait(task)
            return True
        except queue.Full:
            print("Task queue is full.")
            return False
    def get_task(self):
        """Retrieves a task from the queue. Returns None if no tasks are available."""
        try:
            return self._tasks.get_nowait()
        except queue.Empty:
            return None
    def has_tasks(self):
        """Checks if there are tasks remaining in the queue."""
        return not self._tasks.empty()
    def size(self):
        """Returns the number of tasks in the queue."""
        return self._tasks.qsize()

class CriticAgent:
    def __init__(self):
        self.llm = Ollama(model="llama2")
        self.role = colored("Critic Agent: ", "red", attrs=["bold"])
        self.responsibility = '''
        You are a critic agent. You are to determine how well the client's question has been
        answered. Your role is to give a rating from 1 to 10, 1 being incomplete 
        and 10 being complete. You are to provide the rating from 1 to 10 and and explanation
        as to why you gave it that rating.

        '''
    def evaluate(self, prompt):
        interpretation = self.responsibility + prompt 
        response = self.llm.predict(interpretation)
        evaluation = response
        rating = str(Utils.get_first_int(evaluation))
        print("")
        print(self.role + "I am giving that a rating of " + rating + "." + response)
        return evaluation, rating
class RecruitmentAgent:
    def __init__(self):
        self.llm = Ollama(model="llama2")
        self.role = colored("Recruitment Agent: ", "green", attrs=["bold"])
        self.responsibility = '''
        You are a recruitment agent. Your primary role is to take the following task and determine
        which of the following agents would be best fit to complete the task. 

        '''
    def communicate(self, prompt):
        interpretation = self.responsibility + prompt 
        response = self.llm.predict(interpretation)
        print("")
        print(self.role + response)
        critic_agent = CriticAgent()
        evaluation, rating = critic_agent.evaluate(prompt)
        rating = int(rating)
        if rating < 8:
            self.revise(prompt, (evaluation, rating))
        else:
            if rating >= 8:
                MasterAgent.initialize()
    def revise(self, oldResponse, evaluation):
        evaluation_reasoning, rating = evaluation
        interpretation = self.responsibility + " The last response was " + oldResponse + "." + "The feedback about that response is the following: " + evaluation_reasoning + "Fix it." 
        response = self.llm.predict(interpretation)
        print("")
        print(self.role + response)
        critic_agent = CriticAgent()
        evaluation, rating = critic_agent.evaluate(self.role + response)
        rating = int(rating)
        if rating < 8: 
            evaluation, rating = critic_agent.evaluate(self.role + response)
            TaskManagementAgent.revise(self, oldResponse, evaluation)
        else:
            if rating >= 8:
                MasterAgent.initialize()
    def recruit(self): 
        # take in a string of what is the next task
        task = TaskManagementAgent.self.task
        # provide a dictionary all of the agents and what they do and what they are good for. Preferably have all of this in variables.
        agents = {GeneralAgent:"A general agent that can answer questions."}

        # convert agents variable to a string
        agents = str(agents)
        # determine which agent should be used, and why  
        interpretation = self.responsibility + task + agents
        response = self.llm.predict(interpretation)
        print("")
        print(self.role + response)
        critic_agent = CriticAgent()
        evaluation, rating = critic_agent.evaluate(response)
        rating = int(rating)
        if rating < 8:
            self.revise(response, (evaluation, rating))
        else:
            if rating >= 8:

                # logic to somehow connect classnames to the parsed out string name. Might need to be classification model
                agent = classificationmodel(parsed out string)
                # Print the agent it chose to recruit and the reasoning
                reasoning = evaluation 


        interpretation = self.responsibility + " The last response was " + oldResponse + "." + "The feedback about that response is the following: " + evaluation_reasoning + "Fix it." 
                # create an instance of GeneralAgent
                general_agent = GeneralAgent()
                general_agent.communicate(task)


        # return agent name, reasoning. Might need to be attribute as this line might not ever be executed 
class Utils:
    def get_first_int(string):
        # Take a string and return the first integer that is found in the string
        match = re.search(r'\d+', string)
        if match:
            return int(match.group())
        else:
            return None

def main():
    while True:
        try:
            MasterAgent.initialize()
        except KeyboardInterrupt:
            break
if __name__ == "__main__":
    main()

