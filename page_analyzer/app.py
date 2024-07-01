import os

from flask import Flask, render_template, request, url_for, redirect, flash, \
    get_flashed_messages, Response, session
from validators import url

from page_analyzer.db_queries import get_url_info, get_urls_list, get_url_id, \
    insert_url_to_urls, get_url_checks, get_urls_list_with_check_data, \
    insert_check_to_url_checks
from page_analyzer.url_utils import normalize_url, is_exists_url_name

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


@app.route('/', methods=['GET'])
def index() -> str:
    """Handles the GET request to the root URL.

    :return: The rendered HTML template 'index.html' with the flashed messages.
    :rtype: str
    """
    form_value = session.get('url', '')
    session.pop('url', '')
    messages: list[tuple[str, str]] = get_flashed_messages(
        with_categories=True)
    return render_template(
        'index.html',
        messages=messages,
        form_value=form_value
    )


@app.route('/urls/<int:id>', methods=['GET'])
def show_url_page(id: int) -> str:
    """
    Handles the GET request to the '/urls/<id>' URL.

    :param id: The ID of the URL to show.
    :return: str: The rendered HTML template 'show.html' with the URL info.
    """
    session.pop('url', '')
    messages: list[tuple[str, str]] = get_flashed_messages(
        with_categories=True)
    current_url = get_url_info(id)
    current_url_checks = get_url_checks(current_url.name)
    return render_template(
        'show.html',
        id=id,
        name=current_url.name,
        date=current_url.created_at,
        checks=current_url_checks,
        messages=messages
    )


@app.route('/urls/', methods=['GET'])
def show_urls_page() -> str:
    """
    Handles the GET request to the '/urls/' URL.

    :return: The rendered HTML template 'urls.html' with the list of URLs.
    """
    all_urls = get_urls_list_with_check_data()
    return render_template(
        'urls.html',
        urls=all_urls
    )


@app.route('/urls/', methods=['POST'])
def urls_post() -> Response:
    url_value = request.form.get('url')
    session['url'] = url_value
    if url(url_value):
        normalized_url = normalize_url(url_value)
        urls_list = get_urls_list()
        if is_exists_url_name(normalized_url, urls_list):
            flash('Страница уже существует', 'info')
        else:
            insert_url_to_urls(normalized_url)
            flash('Страница успешно добавлена', 'success')
        current_id = get_url_id(normalized_url)
        return redirect(url_for('show_url_page', id=current_id))
    else:
        flash('Некорректный URL', 'danger')
        return redirect(url_for('index'))


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id: int) -> Response:
    insert_check_to_url_checks(id)
    flash('Страница успешно проверена', 'success')
    # flash('Произошла ошибка при проверке', 'danger')
    return redirect(url_for('show_url_page', id=id))


if __name__ == '__main__':
    app.run(debug=False)
