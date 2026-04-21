from flask import Flask,request,jsonify
import sqlite3
app = Flask(__name__)
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        email TEXT NOT NULL
                 )
        """)
    conn.commit()
    conn.close()

init_db()
@app.route("/")
def home():
    return "API IS RUNNING"
@app.route("/users",methods= ["POST"])
def create_user():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    if not username or not email:
        return jsonify({"error": "Invalid input"}), 400

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        (username, email)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "User created"}), 201
@app.route("/users", methods=["GET"])
def get_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, email FROM users")
    rows = cursor.fetchall()

    conn.close()

    users = []
    for row in rows:
        users.append({
            "id": row[0],
            "username": row[1],
            "email": row[2]
        })

    return jsonify(users), 200




if __name__ == '__main__':
    app.run(debug=True
            )

def create_user():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()