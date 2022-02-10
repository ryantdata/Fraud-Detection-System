"""Execute SQL query and return all retrieved records."""


import sqlite3


def fetchall(database, query):
    """Execute SQL query and return all retrieved records.

    Parameters
    ----------
    str database: path to database.

    str query: SQL query string.

    Returns
    -------
    list[tuple] info: returns list of records.
    """
    connection = sqlite3.connect(database)
    mycursor = connection.cursor()
    mycursor.execute(query)
    info = mycursor.fetchall()
    mycursor.close()
    connection.close()

    print('Information successfully retrieved!')

    return info
