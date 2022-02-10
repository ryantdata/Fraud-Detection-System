"""Execute a query that makes changes to sqlite3 database."""


import sqlite3


def commit(database, query):
    """Execute a query that makes changes to sqlite3 database.

    Paramters
    ---------
    str database: path to database.

    str query: SQL query string.

    Returns
    -------
    NoneType None: None.
    """
    connection = sqlite3.connect(database)
    mycursor = connection.cursor()
    mycursor.execute(query)
    connection.commit()
    mycursor.close()
    connection.close()

    print('Changes committed succesfully!')

    return None
