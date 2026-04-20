import sqlite3
def get_connection():
    connection = sqlite3.connect("users.db")
    return connection
def get_users():
   conn = get_connection()
   cursor = conn.cursor()
   cursor.execute("select * from users")
   rows = cursor.fetchall()
   conn.close()
   return rows

def get_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("select * from users where id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def create_user(username , email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("insert into users (username,email) values (?,?)", (username , email))
    conn.commit()
    conn.close()
    return True

def update_user(user_id, username , email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("update users set username = ? , email = ?  where id = ?", (username , email , user_id))
    conn.commit()
    conn.close()


def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("delete from users where id = ?", (user_id,))
    conn.commit()
    conn.close()



