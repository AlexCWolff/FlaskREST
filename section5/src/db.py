import sqlite3
from functools import wraps

def with_db_connection(f):
    """Wrap a function that needs a database connection, perform the query, 
    commit and close the connection."""
    @wraps(f)
    def wrapped(*args, **kwargs):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        f_return = f(cursor, *args, **kwargs)
        connection.commit()
        connection.close()
        return f_return
    return wrapped


@with_db_connection
def init_db(cursor):
    """Initialize the database by creating the table if it does not exists."""
    create_table = (
        'CREATE TABLE IF NOT EXISTS users ('
        'id INTEGER PRIMARY KEY AUTOINCREMENT,'
        'username TEXT NOT NULL,'
        'password TEXT NOT NULL'
        ')'
    )
    cursor.execute(create_table)