from database import get_connection
def get_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("select * from users ")
    rows = cursor.fetchall()
    conn.close()
    result = []
    for row in rows:
        result.append({
            'id': row[0],
            'username': row[1],
            'email': row[2],

        })
    return result

def get_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("select * from users where id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    user = {
        'id': row[0],
        'username': row[1],
        'email': row[2],


    }
    return user
def create_user(username, email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("insert into users (username, email) values (?, ?)", (username, email))
    conn.commit()
    conn.close()

    return True
def update_user(user_id, username, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("select * from users where id =?", (user_id,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return None

    cursor.execute("update users set username = ? , email = ? where id = ?", (username, email, user_id))
    conn.commit()
    conn.close()
    return True

def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("select * from users where id = ?", (user_id,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return None

    cursor.execute("Delete From users Where id = ?", (user_id,))
    conn.commit()
    conn.close()
    return True









