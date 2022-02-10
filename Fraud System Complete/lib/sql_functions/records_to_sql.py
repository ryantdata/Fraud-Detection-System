"""Upload data to sqlite3 database using executemany()."""


import sqlite3


def records_to_sql(database, query, rows):
    """Upload data to sqlite3 database using executemany().

    Paramters
    ---------
    str database: path to database.

    str query: SQL query string.

    list[tuple] rows: records to upload to table.

    Returns
    -------
    NoneType None: None.
    """
    connection = sqlite3.connect(database)
    mycursor = connection.cursor()
    mycursor.executemany(query, rows)
    connection.commit()
    mycursor.close()
    connection.close()

    print('Records committed succesfully!')

    return None
