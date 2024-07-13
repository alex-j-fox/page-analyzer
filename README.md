### Hexlet tests and linter status, Code Climate badge:

[![Actions Status](https://github.com/alex-j-fox/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/alex-j-fox/python-project-83/actions)
[![Actions Status](https://github.com/alex-j-fox/python-project-83/actions/workflows/my-check.yml/badge.svg)](https://github.com/alex-j-fox/python-project-83/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/b2ba41dc47540f37cee1/maintainability)](https://codeclimate.com/github/alex-j-fox/python-project-83/maintainability)

# Page Analyzer

Page Analyzer – is a website that analyzes pages for SEO suitability, similar
to PageSpeed Insights

### Utility features

[//]: # (- нормализует url, проводит его валидацию)

[//]: # (- проверяет вебсайт на доступность и выполняет его SEO-анализ)

[//]: # (- все данные успешных операций добавляются в базу данных)

- normalizes the url and validates it
- checks the website for accessibility and performs its SEO analysis
- all successful operation's data is added to the database

## Installation 

[//]: # (веб-приложению необходимы переменные среды:)

__!!! Web application requires environment variables,__
_which are stored in the file .env (look at [.env.sample](.env.sample))_:

- DATABASE_URL [to connect to the database](https://ru.hexlet.io/blog/posts/python-postgresql),
- SECRET_KEY to ensure application security,


1. Clone the repository

```
git clone https://github.com/alex-j-fox/python-project-83
```

2. Navigate to the project directory 

```
cd /home/<user>/python-project-83
```

3. Create file .env, fill the environment variables with your values

```
echo 'DATABASE_URL=postgresql://<myname>:<mypassword>@localhost:5432/<mydb> 
SECRET_KEY=<mysecretkey>' > .env
```

4. To build and install the package, run the following commands 

```
make install
make build
make dev
```
### Link 
[Page Analyzer](https://python-project-83-mamt.onrender.com/) 