"""Upload CSV data into SQL table."""


import sqlite3
import pandas


def csv_to_sql(filepath, database, table):
    """Upload CSV data into SQL table.

    Parameters
    ----------
    str filepath: path to the CSV data file.

    str database: path to sqlite3 database.

    str table: name of sqlite3 table.

    Returns
    -------
    NoneType None: None.
    """
    import csv

    connection = sqlite3.connect(database)
    mycursor = connection.cursor()

    data = open(filepath)
    row_reader = csv.reader(data)
    csv = pandas.read_csv(filepath)
    columns = csv.columns

    values = ','.join(['?'] * len(columns))
    columns = ','.join(columns)
    query = 'INSERT INTO {} ({}) VALUES ({});'.format(table, columns, values)

    mycursor.executemany(query, row_reader)
    connection.commit()
    mycursor.close()
    connection.close()

    print('Data successfully uploaded!')

    return None
