from flask import Flask, current_app
import pymysql
# from contextlib import contextmanager

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'maestro'
app.config['MYSQL_DB'] = 'user_sys'


# @contextmanager
def connect_to_database():
    """Connects to the database and returns a database connection object."""

    host = current_app.config['MYSQL_HOST']
    user = current_app.config['MYSQL_USER']
    password = current_app.config['MYSQL_PASSWORD']
    db = current_app.config['MYSQL_DB']

    conn = pymysql.connect(host=host, user=user, password=password, db=db)

    try:
        yield conn
    finally:
        conn.close()

    return conn

# Set up the Flask application context
with app.app_context():
    # Connect to the database
    mysql = connect_to_database()

# ...
