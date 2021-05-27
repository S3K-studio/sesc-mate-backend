import psycopg2
from requests import post
from sesc_mate.settings.production import DATABASES


def refresh_users(token):
    db = DATABASES['default']
    connection = psycopg2.connect(dbname=db['NAME'], user=db['USER'],
                                  password=db['PASSWORD'], host=db['HOST'])

    cursor = connection.cursor()

    while True:
        cursor.execute("SELECT vk_user_id FROM api_user LIMIT 250")
        records = list(map(lambda x: str(x[0]), cursor.fetchall()))

        if not len(records):
            break

        users = post(
            'https://api.vk.com/method/users.get',
            params={
                'user_ids': ','.join(records),
                'access_token': token,
                'v': '5.130',
                'fields': 'photo_50',
                'lang': 'ru'
            }
        ).json()['response']

        for user in users:
            cursor.execute('UPDATE api_user SET profile_picture_url = %s WHERE vk_user_id = %s',
                           (user['photo_50'], user['id']))

    connection.commit()
    cursor.close()
    connection.close()
