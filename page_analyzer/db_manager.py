from datetime import date
from functools import wraps

import psycopg2
from psycopg2.extras import NamedTupleCursor


def connect_db(app):
    return psycopg2.connect(app.config['DATABASE_URL'])


def execute_in_db(with_commit=False):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            conn = args[0]
            with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
                result = func(*args, cursor=cursor, **kwargs)
                if with_commit:
                    conn.commit()
                return result

        return inner

    return decorator


@execute_in_db(with_commit=True)
def insert_url_to_urls(conn, url, cursor):
    cursor.execute(
        'INSERT INTO "urls" ("name", "created_at") '
        'VALUES (%s, %s) RETURNING "id"',
        (url, date.today()))
    return cursor.fetchone().id


@execute_in_db()
def get_url_info(conn, id, cursor):
    cursor.execute('SELECT * FROM "urls" WHERE "id"=%s', (id,))
    return cursor.fetchone()


@execute_in_db()
def get_url_id(conn, url, cursor):
    cursor.execute('SELECT * FROM "urls" WHERE "name"=%s', (url,))
    return cursor.fetchone().id


@execute_in_db()
def get_urls_list(conn, cursor):
    cursor.execute('SELECT "name" FROM "urls" ORDER BY "id" DESC')
    return cursor.fetchall()


@execute_in_db(with_commit=True)
def insert_check_to_url_checks(conn, id, url_info, cursor):
    cursor.execute('INSERT INTO "url_checks" ('
                   '"url_id",'
                   '"status_code",'
                   '"h1",'
                   '"title",'
                   '"description",'
                   '"created_at") VALUES (%s, %s, %s, %s, %s, %s)',
                   (id,
                    url_info.status_code,
                    url_info.h1,
                    url_info.title,
                    url_info.description,
                    date.today()))


@execute_in_db()
def get_urls_list_with_check_data(conn, cursor):
    cursor.execute('SELECT DISTINCT ON ("urls"."id") '
                   '"urls"."id", '
                   '"urls"."name", '
                   '"checks"."created_at", '
                   '"checks"."status_code" '
                   'FROM "urls" LEFT JOIN "url_checks" AS "checks" '
                   'ON "urls"."id"="checks"."url_id" '
                   'ORDER BY "urls"."id" DESC , "checks"."id" DESC ')
    return cursor.fetchall()


@execute_in_db()
def get_url_checks(conn, url_id, cursor):
    cursor.execute('SELECT * FROM "url_checks" WHERE "url_id"=%s '
                   'ORDER BY "id" DESC ', (url_id,))
    return cursor.fetchall()
