import hashlib
from lib.database import get_connection

def encrypt_password(password):
    b = bytes(password, encoding='utf-8')
    hash_object = hashlib.sha256(b)
    return hash_object.hexdigest()

def registration(id, name, surname, patronymic, email, password):
    connection = None
    try:
        connection = get_connection()
        password = encrypt_password(password)
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")

            if cursor.rowcount > 0:
                return 'Пользователь с таким Email уже существует'

            cursor.execute(f"INSERT INTO users (id, name, surname, patronymic, email, password, gun_ownership) "
                           f"VALUES('{id}', '{name}', '{surname}', '{patronymic}', '{email}', '{password}', false)")

            connection.commit()
        return None
    finally:
        if connection:
            connection.close()


def auth(email, password):
    connection = None
    user_id = None
    try:
        connection = get_connection()
        password = encrypt_password(password)

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")

            if cursor.rowcount == 0:
                return False, 'Пользователя с таким Email не существует'

            user = cursor.fetchone()
            user_password = user[5]

            if user_password != password:
                return False, 'Указан неверный пароль'

            user_id = user[0]

        return True, user_id
    finally:
        if connection:
            connection.close()


def get_info(id):
    connection = None
    user_json = None
    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE id = '{id}'")

            user = cursor.fetchone()

            user_json = {
                'name': user[1],
                'surname': user[2],
                'patronymic': user[3],
                'email': user[4],
                'type': user[7]
            }

        return user_json
    finally:
        if connection:
            connection.close()


def get_type(id):
    connection = None
    user_json = None
    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE id = '{id}'")

            user = cursor.fetchone()

            user_json = {
                'type': user[7]
            }

        return user_json
    finally:
        if connection:
            connection.close()