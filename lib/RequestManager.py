from lib.database import get_connection


def create_request(id, user_id, service_id, user_fullname, phone_number):
    connection = None
    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            if user_fullname == '':
                user_fullname = "Неавторизованный пользователь"

            cursor.execute(f"INSERT INTO requests VALUES('{id}', '{user_id}', '{service_id}', '{phone_number}', '{user_fullname}')")
            connection.commit()

    finally:
        if connection:
            connection.close()