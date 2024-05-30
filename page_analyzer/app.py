import os

from dotenv import load_dotenv, find_dotenv
from flask import Flask

load_dotenv(find_dotenv())
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return "Hello, Alex!!!"


if __name__ == '__main__':
    app.run(debug=False)
