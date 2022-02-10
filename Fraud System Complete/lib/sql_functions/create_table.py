"""Function creates an sqlite3 table."""


import sqlite3


def create_table(database, columns, table):
    """Create an sqlite3 table.

    Parameters
    ----------
    str database: path to sqlite3 database or path to directory where
                  database is to be created (e.g. dir/filename.filetype).

    str columns: list of columns defined in SQL format.

    str table: name of table to create.

    Returns
    -------
    NoneType None: None.
    """
    query = 'CREATE TABLE %s (%s);' % (table, columns)
    connection = sqlite3.connect(database)
    mycursor = connection.cursor()
    mycursor.execute(query)
    mycursor.close()

    connection.commit()
    connection.close()

    print(f'{table} table successfully created!')

    return None
