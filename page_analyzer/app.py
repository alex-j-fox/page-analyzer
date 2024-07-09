import os

from flask import (Flask, render_template, request, url_for, redirect, flash,
                   Response, session, abort)
from validators import url as validators_url

from page_analyzer import db_manager as db
from page_analyzer.utils import normalize_url, is_exists_url_name

try:
    from dotenv import load_dotenv

    load_dotenv()
except FileNotFoundError:
    pass

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


@app.route('/')
def index() -> str:
    return render_template(
        'index.html',
    )


@app.route('/urls/<int:id>')
def show_url_page(id: int) -> str:
    with db.connect_db(app) as conn:
        current_url = db.get_url_info(conn, id)
        if not current_url:
            abort(404)
        current_url_checks = db.get_url_checks(conn, id)
    return render_template(
        'urls/detail.html',
        url=current_url,
        checks=current_url_checks
    )


@app.route('/urls/')
def show_urls_page() -> str:
    with db.connect_db(app) as conn:
        urls = db.get_urls_list_with_check_data(conn)
    return render_template(
        'urls/list.html',
        urls=urls
    )


@app.post('/urls/')
def handle_url_post_request() -> Response:
    url_value = request.form.get('url')
    session['url'] = url_value
    if len(url_value) > 255:
        flash('URL превышает 255 символов', 'danger')
        return redirect(url_for('index'))

    if not validators_url(url_value):
        flash('Некорректный URL', 'danger')
        return redirect(url_for('index'))

    with db.connect_db(app) as conn:
        normalized_url = normalize_url(url_value)
        urls_list = db.get_urls_list(conn)
        if is_exists_url_name(normalized_url, urls_list):
            flash('Страница уже существует', 'info')
            url_id = db.get_url_id(conn, normalized_url)
        else:
            url_id = db.insert_url_to_urls(conn, normalized_url)
            flash('Страница успешно добавлена', 'success')
        return redirect(url_for('show_url_page', id=url_id))


@app.post('/urls/<int:id>/checks')
def check_url(id: int) -> Response:
    with db.connect_db(app) as conn:
        db.insert_check_to_url_checks(conn, id)
        flash('Страница успешно проверена', 'success')
    # flash('Произошла ошибка при проверке', 'danger')
    return redirect(url_for('show_url_page', id=id))


@app.errorhandler(404)
def page_not_found(_):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(_):
    return render_template('errors/500.html'), 500


if __name__ == '__main__':
    app.run(debug=False)
