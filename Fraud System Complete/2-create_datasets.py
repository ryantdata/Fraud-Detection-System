"""Create preprocessed datasets for model training and testing."""


# packages
import numpy as np
from sklearn.model_selection import train_test_split

# custom functions
from lib.sql_functions.sql_to_pd import sql_to_pd
from lib.sql_functions.records_to_sql import records_to_sql
from lib.sql_functions.tuple_datasets import tuple_datasets
from lib.preprocess_functions.scale import scale


# import data
database = 'database/transactions.db'
table = 'labelled'
query = 'SELECT * FROM {}'.format(table)
labelled_data = sql_to_pd(database=database, query=query)

# Log-transform Amount column
log_labelled = labelled_data.astype(float)
log_labelled.loc[:, 'Amount'] = np.log(log_labelled.loc[:, 'Amount'] + 1)

# seperate class labels
X = log_labelled.drop('Class', axis=1)
y = log_labelled['Class']


# Split data, 50% training, 25% validation, 25% test
x_train, x_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.5,
                                                    random_state=0
                                                    )
x_test, x_val, y_test, y_val = train_test_split(x_test, y_test,
                                                test_size=0.5,
                                                random_state=0
                                                )


# Need to standard scale the data.
cols = ['Transaction_id', 'Time']
scalex_train = scale(x_train, columns=x_train.columns, cols=cols)
scalex_val = scale(x_val, columns=x_val.columns, cols=cols)
scalex_test = scale(x_test, columns=x_test.columns, cols=cols)


# upload datasets to database
columns = ','.join(labelled_data.columns)
values = ','.join(['?'] * (len(labelled_data.columns)))

x_datasets = [scalex_train, scalex_val, scalex_test]
y_datasets = [y_train, y_val, y_test]
tables = ['training', 'test', 'validation']

for i in range(len(x_datasets)):
    query = 'INSERT INTO {} ({}) VALUES ({});'.format(tables[i],
                                                      columns,
                                                      values
                                                      )
    rows = tuple_datasets(x_datasets[i], y_datasets[i])
    records_to_sql(database=database, query=query, rows=rows)
