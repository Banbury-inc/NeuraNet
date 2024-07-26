import json
import os
# Function to extract and print the questions
def print():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'sample_data.json')

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
    json_path = os.path.join(script_dir, 'sample_data.json')
    with open(json_path, 'r') as file:
        squad_data = json.load(file)

    questions = []
    ids = []
    for group in squad_data['data']:
        for passage in group['paragraphs']:
            for qa in passage['qas']:
                questions.append(qa['question'])
                ids.append(qa['id'])
    return questions, ids

def save_predictions(predictions):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    predictions_path = os.path.join('pred.json')
    with open(predictions_path, 'w') as f:
        json.dump(predictions, f)

def get_huggingface_dataset():
    from datasets import load_dataset
    # ds = load_dataset("rajpurkar/squad_v2")
    ds = load_dataset("rajpurkar/squad")
    return ds

def main():
    predictions = {}
    # Get the absolute path to the JSON file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'sample_data.json')

    # Ensure the path is normalized (optional, for safety)
    json_path = os.path.normpath(json_path)

    # Call the function with the correct path
    squad_questions.get()

if __name__ == "__main__":
    main()
