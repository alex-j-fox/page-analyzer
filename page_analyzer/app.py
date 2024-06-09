import datetime
import os
from urllib.parse import urlparse

import psycopg2
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request, url_for, redirect, flash, \
    get_flashed_messages
from psycopg2.extras import DictCursor
from validators import url

load_dotenv(find_dotenv())
DATABASE_URL = os.getenv('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL)


def db_connect():
    try:
        print('Database connected')
        with conn.cursor() as curs, open('database.sql', 'r') as f:
            query = f.read()
            curs.execute(query)
            conn.commit()

    except psycopg2.OperationalError:
        print('Can`t establish connection to database')


db_connect()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/', methods=['GET'])
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html', messages=messages
    )


@app.route('/urls/<id>')
def url_new(id):
    messages = get_flashed_messages(with_categories=True)
    with conn.cursor() as curs:
        curs.execute('SELECT * FROM urls WHERE id=%s', (id,))
        current_url = curs.fetchone()
    return render_template('show.html', id=id, name=current_url[1],
                           date=current_url[2], messages=messages)


@app.post('/urls/')
def urls_post():
    url_value = request.form.get('url')
    if url(url_value):
        parsed_url = urlparse(url_value)
        normalized_url = f'{parsed_url.scheme}://{parsed_url.hostname}'
        with conn.cursor() as curs:
            curs.execute('SELECT * FROM urls')
            all_urls = curs.fetchall()
            name_is_exists = any(normalized_url in _ for _ in all_urls)
            if name_is_exists:
                conn.rollback()
                flash('Страница уже существует', 'info')
            else:
                curs.execute(
                    'INSERT INTO urls (name, created_at) VALUES (%s, %s);',
                    (normalized_url, datetime.date.today()))
                flash('Страница успешно добавлена', 'success')
            curs.execute('SELECT * FROM urls WHERE name=%s;',
                         (normalized_url,))
            current_id = curs.fetchone()[0]

        conn.commit()
        return redirect(url_for('url_new', id=current_id))
    else:
        flash('Некорректный URL', 'danger')
        return redirect(url_for('index'))


@app.route('/urls/')
def urls_get():
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute('SELECT * FROM urls ORDER BY id DESC;')
        all_urls = curs.fetchall()
        return render_template(
            'urls.html',
            urls=all_urls
        )


if __name__ == '__main__':
    app.run(debug=False)
    conn.close()
