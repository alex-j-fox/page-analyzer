from datetime import date
from functools import wraps
from typing import List, Tuple, Any

import psycopg2
from psycopg2.extensions import connection
from psycopg2.extras import NamedTupleCursor


# try:
#     from dotenv import load_dotenv
# 
#     load_dotenv()
# except FileNotFoundError:
#     pass
# 
# DATABASE_URL = os.getenv('DATABASE_URL')


def connect_db(app):
    connection = psycopg2.connect(app.config['DATABASE_URL'])
    return connection


def execute_in_db(with_commit: bool = False):
    """Execute an SQL query in the database.
    Need connect as first argument and cursor

    :param with_commit: Whether to commit the changes to the database.
    :type with_commit: bool
    :return: None
    """

    def decorator(func: callable):

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
def insert_url_to_urls(conn: psycopg2.extensions.connection, url: str,
                       cursor=cursor) -> None:  # noqa: pylint: disable=unused-argument
    """Adds a URL to the "urls" table in the database.

    :param conn: 
    :param url: The URL to add.
    :type url: str
    :return: None
    """
    # with connect_db(DATABASE_URL) as conn, conn.cursor() as curs:
    cursor.execute(
        'INSERT INTO "urls" ("name", "created_at") VALUES (%s, %s);',
        (url, date.today()))
    conn.commit()


def insert_check_to_url_checks(conn: psycopg2.extensions.connection, id: int,
                               cursor=cursor) -> None:  # noqa: pylint: disable=unused-argument
    """Add a new check to the "url_checks" table in the database.

    :param conn: 
    :param id: The ID of the URL to add a check for.
    :type id: int
    :return: None
    """
    # with connect_db(DATABASE_URL) as conn, \
    #         conn.cursor(cursor_factory=NamedTupleCursor) as curs:
    cursor.execute('INSERT INTO "url_checks" ('
                   '"url_id",'
                   # '"status_code",'
                   # '"h1",'
                   # '"title",'
                   # '"description",'
                   '"created_at") VALUES (%s, %s)',
                   (id, date.today()))
    conn.commit()


def get_url_info(conn: psycopg2.extensions.connection, id: int, # noqa: pylint: disable=unused-argument
                 cursor=cursor) -> Tuple[int, str, date]:  # noqa: pylint: disable=unused-argument
    """Get URL info by ID.

    :param id: The URL ID.
    :type id: int
    :return: The URL info or None if not found.
    :rtype: [Tuple[int, str, date]]
    """
    # with connect_db(DATABASE_URL) as conn, \
    #         conn.cursor(cursor_factory=NamedTupleCursor) as curs:
    cursor.execute('SELECT * FROM "urls" WHERE "id"=%s', (id,))
    return cursor.fetchone()


def get_url_id(url: str) -> int:
    """Get ID by URL.

    :param url: The URL to get ID
    :type: str
    :return: The URL ID
    :rtype: int
    """
    with connect_db(DATABASE_URL) as conn, \
            conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('SELECT * FROM "urls" WHERE "name"=%s', (url,))
        return curs.fetchone().id


def get_urls_list() -> List[Tuple[str]]:
    """Get the list of URLs with their IDs, names and creation dates.

    :return: A list of named tuples containing the URL information.
    :rtype: List[Tuple[str]]
    """
    with connect_db(DATABASE_URL) as conn, \
            conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('SELECT "name" FROM "urls" ORDER BY "id" DESC')
        return curs.fetchall()


def get_urls_list_with_check_data() -> List[Tuple[int, str, date, int]]:
    """Get the list of URLs with their check data.
    :return: A list of tuples containing URL ID, name, check creation date, and
     status code.
    :rtype: List[Tuple[int, str, date, int]]
    """
    with connect_db(DATABASE_URL) as conn, \
            conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('SELECT DISTINCT '
                     '"urls"."id", '
                     '"urls"."name", '
                     '"checks"."created_at", '
                     '"checks"."status_code" '
                     'FROM "urls" LEFT JOIN "url_checks" AS "checks" '
                     'ON "urls"."id"="checks"."url_id" '
                     'ORDER BY "urls"."id" DESC')
        return curs.fetchall()


def get_url_checks(url: str) -> List[Tuple[Any, ...]]:
    """Get URL checks by URL.

    :param url: The URL to get checks for.
    :type url: str
    :return: A list of URL checks or None if not found.
    :rtype: Optional[List[UrlItems]]
    """
    with connect_db(DATABASE_URL) as conn, \
            conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('SELECT * FROM "url_checks" WHERE "url_id"=%s '
                     'ORDER BY "created_at" DESC', (get_url_id(url),))
        return curs.fetchall()

# print(get_url_checks('http://rgb.io'))
