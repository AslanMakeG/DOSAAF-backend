from lib.database import get_connection

def create_news(id, name, description):
    connection = None
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO news (id, name, description) "
                           f"VALUES('{id}', '{name}', '{description}')")
            connection.commit()

        return id
    finally:
        if connection:
            connection.close()


def delete_news(id):
    connection = None
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM news WHERE id = '{id}'")
            connection.commit()
    finally:
        if connection:
            connection.close()


def get_all():
    connection = None
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM news")

            news = cursor.fetchall()
            news_list = []
            for one_news in news:
                news_list.append({
                    'id': one_news[0],
                    'name': one_news[1],
                    'description': one_news[2]
                })

            return {'news': news_list}
    finally:
        if connection:
            connection.close()