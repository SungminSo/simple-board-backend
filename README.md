# simple-board-backend

### How to run
- local
    1. git clone https://github.com/SungminSo/simple-board-backend.git
    1. set all of environments
    1. ``` python3 manage.py run ``` or ``` make run ```
    1. expected 
        ``` 
        * Serving Flask app "app" (lazy loading)
        * Environment: dev
        * Debug mode: off
        * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
        
       ```
       
### How to install packages
```
make install
```
or
``` 
make install-dev
```

       
### Env
|key                |value           |
|-------------------|----------------|
|POSTGRES_HOST      |localhost       |
|POSTGRES_PORT      |5432            |
|POSTGRES_USER      |paul            |
|POSTGRES_DB_NAME   |board           |
|POSTGRES_PASSWORD  |password        |
|USER_JWT_SECRET_KEY|qwerasdfzxcv1234|

### API
Postman: <a href="https://documenter.getpostman.com/view/4736816/TVCiT6Jd">Docs</a>\
Wiki: <a href="https://github.com/SungminSo/simple-board-backend/wiki/API-List">API List</a>

### DB
Wiki: <a href="https://github.com/SungminSo/simple-board-backend/wiki/DB-Models">DB model</a>

### Project Structure
```
- app
    - models
        - __init__.py
        - articles.py
        - boards.py
        - logout.py
        - users.py
    - shared
        - __init__.py
        - config.py
    - views
        - __init__.py
        - articles.py
        - boards.py
        - user.py
    - __init__.py
    - config.py
- migrations
    - versions
        - ...
    - alembic.ini
    - env.py
    - README
    - script.py.mako
- .gitignore
- manage.py
- Pipfile
- Pipfile.lock
- READEM.md
```
