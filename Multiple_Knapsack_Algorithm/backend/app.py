from flask import Flask, request, jsonify
from api import user_management
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Return values:
'''
Authenticate user log in
Enpoint:/authenticate
Method: GET
Response Format: JSON

Request:
'username' (string, required): The username of the user
'password' (string, required): The password of the user

Response:
Status: 200 OK
Example Response:
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
            "last_name": user_data[3],
            "devices" : user_data[4]
        }
        return jsonify(response_data)
    else:
        return jsonify({"message": "Authentication failed"}), 401
    
'''
Get a file from IPFS
Enpoint:/get_from_ipfs
Method: GET
Response Format: JSON

Request:
'cid' (string, required): The file's CID

Response:
Status: 200 OK
Example Response:
{
  "first_name": "Michael",
  "last_name": "Mills",
  "userID": "d42e82de-f5de-4dfc-be94-d9872f0385d0",
  "username": "john_doe"
}
'''
@app.route("/get_from_ipfs")
def get_from_ipfs():
    cid = request.args.get('cid')

    if not cid:
        return jsonify({"message": "Missing cid"}), 400

    user_data = user_management.get_from_ipfs(cid)
    
    return jsonify(user_data)

 
if __name__ == "__main__":
    app.run(debug=True)