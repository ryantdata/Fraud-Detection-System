"""."""


import sqlite3
import datetime as dt


def upload_synth_data(sample, prediction):
    """."""
    connection = sqlite3.connect('transactions.db')
    mycursor = connection.cursor()

    columns = ['Time', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8',
               'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17',
               'V18', 'V19', 'V20', 'V21', 'V22', 'V23', 'V24', 'V25', 'V26',
               'V27', 'V28', 'Amount', 'Class']
    values = ','.join(['?'] * len(columns))
    columns = ','.join(columns)

    sample = sample.tolist()
    sample.append(prediction)
    # time will differ from time shown on dashboard as this function is
    # retrofit to the app.
    sample.insert(0, dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    if sample[30] == 1:
        table = 'flagged'
        query = 'INSERT INTO {} ({}) VALUES ({});'.format(table,
                                                          columns,
                                                          values
                                                          )
        mycursor.execute(query, sample)
        connection.commit()

    if sample[30] == 0:
        table = 'unflagged'
        query = 'INSERT INTO {} ({}) VALUES ({});'.format(table,
                                                          columns,
                                                          values
                                                          )
        mycursor.execute(query, sample)
        connection.commit()

    table = 'synthetic'
    query = 'INSERT INTO {} ({}) VALUES ({});'.format(table,
                                                      columns,
                                                      values
                                                      )
    mycursor.execute(query, sample)
    connection.commit()
    mycursor.close()
    connection.close()

    return None
