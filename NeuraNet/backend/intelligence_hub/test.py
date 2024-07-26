import main
import termcolor
from config import Config 
from utils import Utils 
from benchmarks import squad_questions 
from datasets import load_dataset

'''
Make sure show agent dialogue is set to false in Config file before running

SQuAD benchmark estimated to take around 6 hours. 
'''

# count the number of questions




ds = squad_questions.get_huggingface_dataset()
train_dataset = ds['train']
total_number_of_questions = len(train_dataset)
print("Total number of questions: ", total_number_of_questions)



predictions = {}
question_number = 0
if Config.run_squad_benchmark == True:
    for dataset_question in train_dataset:
        question_number = question_number + 1
        question_number_print_statement = f"{question_number}/{total_number_of_questions}"
        context = str(dataset_question['context'])
        question = str(dataset_question['question'])
        answer = str(dataset_question['answers']['text'][0])
        id = str(dataset_question['id'])
        print("\n")

        colored_question = termcolor.colored("Context: ", "green")
        colored_id = termcolor.colored("ID: ", "green")
        colored_question_number = termcolor.colored("Context Number: ", "green")
        print(colored_id, id)
        print(colored_question_number, question_number_print_statement)
        print(colored_question, context)

        colored_question = termcolor.colored("Question: ", "green")
        colored_id = termcolor.colored("ID: ", "green")
        colored_question_number = termcolor.colored("Question Number: ", "green")
        print(colored_question, question)


        colored_answer = termcolor.colored("Answwer: ", "green")
        print(colored_answer, answer)

        instructions = "Use the following pieces of context to answer the question. Only provide the answer to the question, you don't even need a full sentence."
        prompt = instructions + question + context
        colored_response = termcolor.colored("Response: ", "green")
        response = main.run_as_function(prompt)
        print(colored_response, response)

        predictions[id] = response
        squad_questions.save_predictions(predictions)

        f1 = Utils.f1_score(response, answer)
        colored_f1 = termcolor.colored("F1 Score: ", "green")
        print(colored_f1, f1)


