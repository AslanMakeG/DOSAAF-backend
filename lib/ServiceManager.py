from lib.database import get_connection

def create_service(id, name, description, cost):
    connection = None
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO services (id, name, description, cost) "
                           f"VALUES('{id}', '{name}', '{description}', {cost})")

            connection.commit()

        return id
    finally:
        if connection:
            connection.close()


def delete_service(id):
    connection = None
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM services WHERE id = '{id}'")

            connection.commit()
    finally:
        if connection:
            connection.close()


def get_all():
    connection = None
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM services")

            services = cursor.fetchall()
            service_list = []
            for service in services:
                service_list.append({
                    'id': service[0],
                    'name': service[1],
                    'description': service[2],
                    'cost': service[3]
                })

            return {'services': service_list}
    finally:
        if connection:
            connection.close()