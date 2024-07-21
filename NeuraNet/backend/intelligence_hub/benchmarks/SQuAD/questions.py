import json
import os
# Function to extract and print the questions
def print():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'train-v2.0.json')

    with open(json_path, 'r') as file:
        squad_data = json.load(file)

    questions = []
    for group in squad_data['data']:
        for passage in group['paragraphs']:
            for qa in passage['qas']:
                questions.append(qa['question'])
                print(qa['question'])
    return questions

# Function to extract and print the questions
def get():

    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'train-v2.0.json')
    with open(json_path, 'r') as file:
        squad_data = json.load(file)

    questions = []
    for group in squad_data['data']:
        for passage in group['paragraphs']:
            for qa in passage['qas']:
                questions.append(qa['question'])
    return questions

def main():
    # Get the absolute path to the JSON file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'train-v2.0.json')

    # Ensure the path is normalized (optional, for safety)
    json_path = os.path.normpath(json_path)

    # Call the function with the correct path
    get()

if __name__ == "__main__":
    main()
