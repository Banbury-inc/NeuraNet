import jwt
import datetime
from flask import request, jsonify, current_app
from functools import wraps

# Replace this secret key with a strong and random string in a production environment
SECRET_KEY = "your-secret-key"

# Function to generate an access token
def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiration time (1 hour in this example)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# Decorator to protect API endpoints with authentication
def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token["user_id"]
            # You can use user_id for further user-specific operations here
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated
