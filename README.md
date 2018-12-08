OkoaJamii
===

A Flask web application that features an online reporting tool as well as an online case management platform.

Getting Started
===

Install virtualenv in your machine if you don't have one yet.

```
pip install virtualenv
```

Create virtualenv directory inside the project folder

```
virtualenv venv
```

Activate your virtual environment from the Scripts folder.

```
cd venv/Scripts
```

```
activate
```

Install the library and module requirements from the main directory

```
pip install -r requirements.txt
```

And now you should be good to go. To run the Flask server use the following command:

```
python manage.py runserver.

```
To run shell:

```
python manage.py shell
```


To create the database and tables:

Install postgres on your computer and its dependencies e.g psycopg2

Create a new user/password and database as they appear in config.py file (adminuser/hardtocrackpassword) db (Main)

on command prompt run
```
python manage.py shell

from app import db

db.create_all()
```

Built With
===

Python 3.6  
[Flask](http://flask.pocoo.org/docs/0.12/) 
[Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)  
[Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)  


Author
===

Imran Abdallah
