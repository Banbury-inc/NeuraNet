from flask import Flask, request, jsonify
from api import user_management
from flask_cors import CORS
from api import files
from flask_sqlalchemy import SQLAlchemy
from api import user_management_mysql


app = Flask(__name__)
CORS(app)


# Configure SQLAlchemy for MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mmills6060:Dirtballer!6060@localhost:3306/banburye_users'
db = SQLAlchemy()
db.init_app(app)

``



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

@app.route("/test_database")
def test_database():
    """Tests the connection to the database and returns a message indicating whether the connection was successful or not."""

    message = user_management_mysql.test_database_connection()
    return jsonify(message)


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

existing_user_data_map_cid = ["QmTYuuAqSv48CQsAz7hhG3NjStuvXzMkYsYLYWfRY8L23D"]
global next_user_data_map_cid
next_user_data_map = []

@app.route("/update_users_with_arguments")
def update_users_with_arguments():
    global next_user_data_map_cid
    username = request.args.get('username')
    cid = request.args.get('cid')
    # Call your function to obtain the new CID
    cid = user_management.update_user_data_map_with_arguments(username, cid)

    # Convert the CID to a string and store it in next_user_data_map
    string_cid = str(cid)
    
    next_user_data_map.insert(0, string_cid)

    # Update next_user_data_map_cid to be equal to next_user_data_map
    next_user_data_map_cid = next_user_data_map.copy()

    return jsonify(next_user_data_map_cid)    
    
@app.route("/update_users")
def update_users():
    global next_user_data_map_cid

    # Call your function to obtain the new CID
    cid = user_management.update_user_data_map()

    # Convert the CID to a string and store it in next_user_data_map
    string_cid = str(cid)
    
    next_user_data_map.insert(0, string_cid)

    # Update next_user_data_map_cid to be equal to next_user_data_map
    next_user_data_map_cid = next_user_data_map.copy()

    return jsonify(next_user_data_map_cid)

@app.route("/users")
def get_users():
    if next_user_data_map:
        return jsonify(next_user_data_map)
    else:
        return jsonify(existing_user_data_map_cid)
        
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


@app.route("/register")
def register():
    username = request.args.get('username')
    password = request.args.get('password')
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    devices_list = request.args.get('devices_list')
    file_info_list = request.args.get('file_info_list')

    register_user_add_to_user_data_map(username, password, first_name, last_name, devices_list, file_info_list)

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

'''
Get all files that are owned by a user
Enpoint:/get_files
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

# Sample data (in a real application, this data might come from a database)
files = [
    {"id": 1, "name": 'File 1', "size": 50, "priority": 3},
    {"id": 2, "name": 'File 2', "size": 30, "priority": 2},
    # Add more files here
]



@app.route("/get_file_info")
def get_files():
    cid = request.args.get('cid')

    if not cid:
        return jsonify({"message": "Missing cid"}), 400

    user_files = user_management.get_from_ipfs(cid)
    

    return jsonify(files)


if __name__ == "__main__":
    app.run(debug=True)