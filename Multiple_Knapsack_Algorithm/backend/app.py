from flask import Flask, request, jsonify
from api import user_management
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Return values:
'''
{
  "first_name": "Michael",
  "last_name": "Mills",
  "userID": "d42e82de-f5de-4dfc-be94-d9872f0385d0",
  "username": "john_doe"
}
'''
@app.route("/authenticate")
def authenticate():
    username = request.args.get('username')
    password = request.args.get('password')
#    username = "john_doe"
#    password = "secretpassword"
    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    user_data = user_management.authenticate_user(username, password)
    
    if user_data:
        response_data = {
            "userID": user_data[0],
            "username": user_data[1],
            "first_name": user_data[2],
            "last_name": user_data[3]
        }
        return jsonify(response_data)
    else:
        return jsonify({"message": "Authentication failed"}), 401
    

if __name__ == "__main__":
    app.run(debug=True)