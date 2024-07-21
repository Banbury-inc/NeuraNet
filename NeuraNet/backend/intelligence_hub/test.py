import main
from benchmarks.SQuAD import questions
import termcolor

'''
Make sure show agent dialogue is set to false in Config file before running
'''

questions = questions.get()
for question in questions:

    print("\n\n")
    colored_question = termcolor.colored("Question: ", "green")
    print(colored_question, question)

    print("\n\n")
    response = main.run_as_function(question)
    print(response)

