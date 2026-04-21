from flask import Flask, jsonify, request
import hashlib
import sqlite3
import jwt
import datetime

app = Flask(__name__)

SECRET_KEY = "mysecret123"


def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users_auth (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/")
def home():
    return "Auth API running"


@app.route("/register", methods=["POST"])
def register():
    req = request.get_json()
    if not req:
        return jsonify({"error": "Invalid JSON body"}), 400

    email = req.get("email")
    password = req.get("password")

    if not email or not password:
        return jsonify({"error": "Email or password is required"}), 400

    password = hashlib.md5(password.encode()).hexdigest()

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users_auth WHERE email = ?", (email,))
    existing = cursor.fetchone()

    if existing:
        conn.close()
        return jsonify({"error": "Email already registered"}), 400

    cursor.execute(
        "INSERT INTO users_auth (email, password) VALUES (?, ?)",
        (email, password)
    )

    conn.commit()
    conn.close()

    return jsonify({"success": "User registered successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    req = request.get_json()
    if not req:
        return jsonify({"error": "Invalid JSON body"}), 400

    email = req.get("email")
    password = req.get("password")

    if not email or not password:
        return jsonify({"error": "Email or password is required"}), 400

    password = hashlib.md5(password.encode()).hexdigest()

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users_auth WHERE email = ? AND password = ?",
        (email, password)
    )

    existing = cursor.fetchone()
    conn.close()

    if not existing:
        return jsonify({"error": "Invalid email or password"}), 400

    payload = {
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return jsonify({
        "success": True,
        "token": token
    }), 200


@app.route("/me", methods=["GET"])
def me():
    token = request.headers.get("token")

    if not token:
        return jsonify({"error": "unauthorized"}), 401

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = data.get("email")
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "unauthorized"}), 401

    return jsonify({"email": email}), 200


@app.route("/profile", methods=["GET"])
def profile():
    token = request.headers.get("token")

    if not token:
        return jsonify({"error": "unauthorized"}), 401

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = data.get("email")
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "unauthorized"}), 401

    return jsonify({"message": f"welcome {email}"}), 200


@app.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "logged out"}), 200


@app.route("/create_note", methods=["POST"])
def create_note():
    token = request.headers.get("token")

    if not token:
        return jsonify({"error": "unauthorized"}), 401

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = data.get("email")
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "unauthorized"}), 401

    req = request.get_json()
    if not req:
        return jsonify({"error": "Invalid JSON body"}), 400

    content = req.get("content")

    if not content:
        return jsonify({"error": "content is required"}), 400

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO notes (email, content) VALUES (?, ?)",
        (email, content)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "note created"}), 201


@app.route("/get_notes", methods=["GET"])
def get_notes():
    token = request.headers.get("token")

    if not token:
        return jsonify({"error": "unauthorized"}), 401

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = data.get("email")
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "unauthorized"}), 401

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT content FROM notes WHERE email = ?",
        (email,)
    )

    notes = cursor.fetchall()
    conn.close()

    notes_list = [n[0] for n in notes]

    return jsonify({"notes": notes_list}), 200


@app.route("/delete_note", methods=["POST"])
def delete_note():
    token = request.headers.get("token")

    if not token:
        return jsonify({"error": "unauthorized"}), 401

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = data.get("email")
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "unauthorized"}), 401

    req = request.get_json()
    if not req:
        return jsonify({"error": "Invalid JSON body"}), 400

    content = req.get("content")

    if not content:
        return jsonify({"error": "content is required"}), 400

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM notes WHERE email = ? AND content = ?",
        (email, content)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "note deleted"}), 200


@app.route("/update_note", methods=["POST"])
def update_note():
    token = request.headers.get("token")

    if not token:
        return jsonify({"error": "unauthorized"}), 401

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = data.get("email")
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "unauthorized"}), 401

    req = request.get_json()
    if not req:
        return jsonify({"error": "Invalid JSON body"}), 400

    old_content = req.get("old_content")
    new_content = req.get("new_content")

    if not old_content or not new_content:
        return jsonify({"error": "old_content and new_content are required"}), 400

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE notes SET content = ? WHERE email = ? AND content = ?",
        (new_content, email, old_content)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "note updated"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5002)