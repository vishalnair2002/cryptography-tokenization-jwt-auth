from flask import Flask, request, jsonify
import jwt
import datetime
import bcrypt

app = Flask(__name__)

SECRET_KEY = "my_super_secure_key"

# Hashed password storage
password = bcrypt.hashpw("2002".encode('utf-8'), bcrypt.gensalt())

USER_DATA = {
    "username": "Vishal",
    "password": password,
    "role": "admin"
}

# Token blacklist
blacklisted_tokens = []

# Generate Access Token
def generate_access_token(username, role):
    payload = {
        "user": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# Generate Refresh Token
def generate_refresh_token(username):
    payload = {
        "user": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }

    refresh_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return refresh_token

# LOGIN ROUTE
@app.route('/login', methods=['POST'])
def login():

    auth = request.json

    if auth["username"] == USER_DATA["username"] and bcrypt.checkpw(
        auth["password"].encode('utf-8'),
        USER_DATA["password"]
    ):

        access_token = generate_access_token(
            auth["username"],
            USER_DATA["role"]
        )

        refresh_token = generate_refresh_token(
            auth["username"]
        )

        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token
        })

    return jsonify({"message": "Invalid credentials"}), 401

# PROTECTED ROUTE
@app.route('/protected', methods=['GET'])
def protected():

    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"message": "Token missing"}), 403

    if token.startswith("Bearer "):
        token = token[7:]

    if token in blacklisted_tokens:
        return jsonify({"message": "Token has been revoked"}), 401

    try:
        decoded = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return jsonify({
            "message": "Access granted",
            "user": decoded
        })

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired"}), 401

    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401

# REFRESH TOKEN ROUTE
@app.route('/refresh', methods=['POST'])
def refresh():

    refresh_token = request.json.get("refresh_token")

    try:
        decoded = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        new_access_token = generate_access_token(
            decoded["user"],
            "admin"
        )

        return jsonify({
            "access_token": new_access_token
        })

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Refresh token expired"}), 401

    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid refresh token"}), 401

# LOGOUT ROUTE
@app.route('/logout', methods=['POST'])
def logout():

    token = request.headers.get("Authorization")

    if token.startswith("Bearer "):
        token = token[7:]

    blacklisted_tokens.append(token)

    return jsonify({
        "message": "Logged out successfully"
    })

# RUN APPLICATION
if __name__ == '__main__':
    app.run(debug=True)