from flask import Flask

app = Flask(__name__)

# Importing the API endpoints
from api import devices, files ## knapsack

if __name__ == "__main__":
    app.run()
