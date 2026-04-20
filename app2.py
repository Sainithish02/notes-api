import email

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/users", methods=["GET"])
def get_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    conn.close()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "username": row[1],
            "email": row[2]
        })

    return jsonify(result), 200


@app.route("/users", methods=["POST"])
def create_user():
    username = request.json.get("username")
    email = request.json.get("email")

    if not username or not email:
        return jsonify({"error": "Invalid input"}), 400

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("select * FROM users WHERE email = ?", (email,))
    existing = cursor.fetchone()
    if existing:
        return jsonify({"error": "User already exists"}), 400

    cursor.execute(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        (username, email)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "User created"}), 201


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, email FROM users WHERE id = ?",
        (user_id,)
    )
    row = cursor.fetchone()

    conn.close()

    if row is None:
        return jsonify({"error": "User not found"}), 404

    user = {
        "id": row[0],
        "username": row[1],
        "email": row[2]
    }

    return jsonify(user), 200

@app.route("/users/email/<email>", methods=["GET"])
def get_user_by_email(email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, email FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()

    conn.close()

    if row is None:
        return jsonify({"error": "User not found"}), 404

    user = {
        "id": row[0],
        "username": row[1],
        "email": row[2]
    }

    return jsonify(user), 200


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    username = request.json.get("username")
    email = request.json.get("email")

    if not username or not email:
        return jsonify({"error": "Invalid input"}), 400

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET username = ?, email = ? WHERE id = ?",
        (username, email, user_id)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "User updated"}), 200


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))

    conn.commit()
    conn.close()

    return jsonify({"message": "User deleted"}),200
@app.route("/users/check-email/<email>", methods = ["GET"])
def check_email(email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return jsonify({"exists" : False}), 200
    return jsonify({"exists" : True}), 200



if __name__ == "__main__":
    app.run(debug=True, port=5001)

