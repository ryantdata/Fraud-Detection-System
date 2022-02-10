"""Pull data from sqlite3 table into pandas DataFrame."""


import sqlite3
import pandas


def sql_to_pd(database, query):
    """Pull data from sqlite3 table into pandas DataFrame.

    Parameters
    ----------
    str database: path to sqlite3 database.

    str query: SQL query string.

    Returns
    -------
    pd.DataFrame data: Requested data from sqlite3 table.
    """
    connection = sqlite3.connect(database)
    data = pandas.read_sql(con=connection, sql=query)

    print('Data successfully retrieved!')

    return data
