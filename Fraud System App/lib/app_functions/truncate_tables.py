"""Delete data from specified sql tables."""


from lib.sql_functions.commit import commit


def truncate_tables():
    """Delete data from specified sql tables.

    Parameters
    ----------
    None

    Returns
    -------
    NoneType None: None.
    """
    database = 'transactions.db'
    tables = ['synthetic', 'flagged', 'unflagged']

    for i in tables:
        query = 'DELETE FROM %s' % (i)
        commit(database, query)

    return None
