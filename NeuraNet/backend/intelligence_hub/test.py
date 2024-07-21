import main
from benchmarks.SQuAD import squad_questions
import termcolor
import json
from config import Config 

'''
Make sure show agent dialogue is set to false in Config file before running

SQuAD benchmark estimated to take around 6 hours. 
'''

# count the number of questions

questions, ids = squad_questions.get()
total_number_of_questions = len(questions)
print("Total number of questions: ", total_number_of_questions)

predictions = {}
question_number = 0
if Config.run_squad_benchmark == True:
    for question, id in zip(questions, ids):
        question_number = question_number + 1
        question_number_print_statement = f"{question_number}/{total_number_of_questions}"
        print("\n\n")
        colored_question = termcolor.colored("Question: ", "green")
        colored_id = termcolor.colored("ID: ", "green")
        colored_question_number = termcolor.colored("Question Number: ", "green")
        print(colored_question, question)
        print(colored_id, id)
        print(colored_question_number, question_number_print_statement)

        print("\n\n")
        response = main.run_as_function(question)
        print(response)

        predictions[id] = response

        squad_questions.save_predictions(predictions)
