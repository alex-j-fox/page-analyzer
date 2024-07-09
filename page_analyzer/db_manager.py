from datetime import date
from functools import wraps

import psycopg2
from psycopg2.extensions import connection
from psycopg2.extras import NamedTupleCursor



def connect_db(app):
    return psycopg2.connect(app.config['DATABASE_URL'])


def execute_in_db(with_commit=False):
   
    def decorator(func):

        @wraps(func)
        def inner(*args, **kwargs):
            conn = args[0]
            if not isinstance(conn, psycopg2.extensions.connection):
                raise ValueError('First argument must be psycopg2 connection')
            try:
                with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
                    result = func(cursor=cursor, *args, **kwargs)
                    if with_commit:
                        conn.commit()
                    return result
            except Exception as e:
                conn.rollback()
                raise e

        return inner

    return decorator


@execute_in_db(with_commit=True)
def insert_url_to_urls(conn, url, cursor):  # noqa: pylint: disable=unused-argument
    cursor.execute(
        'INSERT INTO "urls" ("name", "created_at") VALUES (%s, %s) RETURNING "id";',
        (url, date.today()))
    conn.commit()


@execute_in_db()
def get_url_info(conn, id, cursor):  # noqa: pylint: disable=unused-argument
    cursor.execute('SELECT * FROM "urls" WHERE "id"=%s', (id,))
    return cursor.fetchone()


@execute_in_db()
def get_url_id(conn, url, cursor):  # noqa: pylint: disable=unused-argument
    cursor.execute('SELECT * FROM "urls" WHERE "name"=%s', (url,))
    return cursor.fetchone().id


@execute_in_db()
def get_urls_list(conn, cursor):  # noqa: pylint: disable=unused-argument
    cursor.execute('SELECT "name" FROM "urls" ORDER BY "id" DESC')
    return cursor.fetchall()


@execute_in_db(with_commit=True)
def insert_check_to_url_checks(conn, id, cursor):  # noqa: pylint: disable=unused-argument
    cursor.execute('INSERT INTO "url_checks" ('
                   '"url_id",'
                   # '"status_code",'
                   # '"h1",'
                   # '"title",'
                   # '"description",'
                   '"created_at") VALUES (%s, %s)',
                   (id, date.today()))
    conn.commit()


@execute_in_db()
def get_urls_list_with_check_data(conn, cursor ):  # noqa: pylint: disable=unused-argument
    cursor.execute('SELECT DISTINCT '
                 '"urls"."id", '
                 '"urls"."name", '
                 '"checks"."created_at", '
                 '"checks"."status_code" '
                 'FROM "urls" LEFT JOIN "url_checks" AS "checks" '
                 'ON "urls"."id"="checks"."url_id" '
                 'ORDER BY "urls"."id" DESC')
    return cursor.fetchall()


@execute_in_db()
def get_url_checks(conn, url_id, cursor):  # noqa: pylint: disable=unused-argument
    cursor.execute('SELECT * FROM "url_checks" WHERE "url_id"=%s '
                 'ORDER BY "created_at" DESC', (url_id,))
    return cursor.fetchall()
