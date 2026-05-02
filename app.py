from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)

SECRET_KEY = "my_secret_key"

# Dummy user data (for demonstration)
USER_DATA = {
    "username": "Vishal",
    "password": "2002"
}

# Function to generate token
def generate_token(username):
    payload = {
        "user": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    auth = request.json

    if auth["username"] == USER_DATA["username"] and auth["password"] == USER_DATA["password"]:
        token = generate_token(auth["username"])
        return jsonify({"token": token})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Protected endpoint
@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get("Authorization")

    if token and token.startswith("Bearer "):
        token = token[7:]

    if not token:
        return jsonify({"message": "Token missing"}), 403

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"message": "Access granted", "user": decoded})
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401

# Run server
if __name__ == '__main__':
    app.run(debug=True)