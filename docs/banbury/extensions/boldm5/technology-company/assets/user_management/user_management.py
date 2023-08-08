from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/run-python-script', methods=['GET'])
def run_python_script():
    # Get data from the request
    data = request.json

    # Run the Python script
    result = run_my_python_script(data['param'])

    return jsonify({'result': result})

def run_my_python_script(param):
    # Your Python code here
    result = f'Hello from Python! Received param: {param}'
    return result

if __name__ == '__main__':
    app.run(debug=True)
