from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# ----------------- DATABASE -----------------
client = MongoClient("mongodb://localhost:27017/")
db = client["finance_db"]
users = db["users"]

# ----------------- SIGN UP -----------------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "All fields required"})

    if users.find_one({"username": username}):
        return jsonify({"success": False, "message": "User already exists"})

    hashed_pw = generate_password_hash(password)

    users.insert_one({
        "username": username,
        "password": hashed_pw
    })

    return jsonify({"success": True})


# ----------------- LOGIN -----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = users.find_one({"username": username})

    if not user:
        return jsonify({"success": False, "message": "User not found"})

    if not check_password_hash(user["password"], password):
        return jsonify({"success": False, "message": "Wrong password"})

    return jsonify({"success": True})


# ----------------- RUN SERVER -----------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
