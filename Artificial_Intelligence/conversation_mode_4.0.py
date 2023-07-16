from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType, load_tools
from langchain.utilities import WikipediaAPIWrapper, PythonREPL, TextRequestsWrapper, GoogleSearchAPIWrapper
from langchain.tools import ShellTool
from langchain.agents.agent_toolkits import GmailToolkit
from langchain.tools.gmail.utils import build_resource_service, get_gmail_credentials
from langchain.tools.file_management import (
    ReadFileTool,
    CopyFileTool,
    DeleteFileTool,
    MoveFileTool,
    WriteFileTool,
    ListDirectoryTool,
)
from langchain.agents.agent_toolkits import FileManagementToolkit
from tempfile import TemporaryDirectory
import os

os.environ["GOOGLE_CSE_ID"] = "9257a94d07b114416"
os.environ["GOOGLE_API_KEY"] = "AIzaSyBfMrZ2bkFbh-CGIMM2zHzROJQevxNSaVs"
OPENAI_API_KEY = "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"
llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo', openai_api_key=OPENAI_API_KEY)
def test(prompt):
    python_repl = PythonREPL()
    requests_tools = load_tools(["requests_all"])
    # Each tool wrapps a requests wrapper
    requests_tools[0].requests_wrapper
    TextRequestsWrapper(headers=None, aiosession=None)
    requests = TextRequestsWrapper()
    # We'll make a temporary directory to avoid clutter
    working_directory = TemporaryDirectory()
    toolkit = FileManagementToolkit(root_dir=str(working_directory.name), selected_tools=["read_file", "write_file", "list_directory"]).get_tools()
    read_tool, write_tool, list_tool = toolkit
    wikipedia = WikipediaAPIWrapper()
    shell_tool = ShellTool()
    search= GoogleSearchAPIWrapper()

    
    tools = [
        Tool(
            name="Wikipedia",
            func=wikipedia.run,
            description="Useful for when you need to get information from wikipedia about a single topic"
        ),
        Tool(
            name="ShellTool",
            func=shell_tool.run,
            description="Executes commands in a terminal. Input should be valid commands, and the output will be any output from running that command."
        ),
         Tool(
            name="list_directory",
            func=list_tool.run,
            description="Interact with the local file system. List the files in a directory."
        ),
        Tool(
            name="python_rep1",
            func=python_repl.run,
            description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`."
        ),
#         Tool(
#            name="requests",
#            func=requests.get,
#            description="A portal to the internet. Use this when you need to get specific content from a site. Input should be a specific url, and the output will be all the text on that page."
#        ),
        Tool(
            name="Google Search",
            func=search.run,
            description="Search Google for recent results"
        )

    ]
    agent_executor = initialize_agent(tools, llm, agent='zero-shot-react-description', verbose=True)
    output = agent_executor.run(prompt)
    print (output)
def main():
    prompt = input("---->")
    test(prompt)
if __name__ == '__main__':
    main()
