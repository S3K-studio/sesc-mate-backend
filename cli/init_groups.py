import psycopg2
from sesc_mate.settings.production import DATABASES


def fill_groups():
    db = DATABASES['default']

    connection = psycopg2.connect(dbname=db['NAME'], user=db['USER'],
                                  password=db['PASSWORD'], host=db['HOST'])
    cursor = connection.cursor()

    for group in range(1, 33):
        cursor.execute("INSERT INTO notification_bot_group (group_number) VALUES (%s)", (group, ))

    connection.commit()
    cursor.close()
    connection.close()
