import psycopg2



conn = psycopg2.connect(
    dbname="",      # имя вашей базы данных
    user="",        # имя пользователя PostgreSQL
    password="",    # пароль
    host="",        # обычно localhost
    port=""         # обычно 5432
)


conn.autocommit = True



def create(name, email):
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;",
            (name, email)
        )
        return cursor.fetchone()[0]



def read_all():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users;")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]



def update(user_id, fields):
    set_clause = ", ".join(f"{key} = %s" for key in fields.keys())
    values = list(fields.values()) + [user_id]

    query = f"UPDATE users SET {set_clause} WHERE id = %s;"

    with conn.cursor() as cursor:
        cursor.execute(query, values)



def delete(user_id):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))



if __name__ == "__main__":
    user_id = create("Иван", "ivan@test.ru")
    print("После CREATE:", read_all())

    update(user_id, {"email": "new_ivan@test.ru"})
    print("После UPDATE:", read_all())

    delete(user_id)
    print("После DELETE:", read_all())
