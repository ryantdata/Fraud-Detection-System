"""Database for the project is created using this script."""

# packages
import pandas as pd

# custom functions
from lib.sql_functions.create_table import create_table
from lib.sql_functions.csv_to_sql import csv_to_sql


# Data needed to be split into smaller files so that it could be uploaded
# onto github. This bit of code recombines the data into a single CSV file
# for the project.
data1 = pd.read_csv("data/creditcard1.csv")
data2 = pd.read_csv("data/creditcard2.csv")
data = pd.concat([data1, data2])
data = data.drop('Unnamed: 0', axis=1)

data.to_csv("data/creditcard.csv", index=False)


# All tables in the database use the same datatypes.

# Define columns.
columns = '''
Transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
 Time VARCHAR(50),
 V1 DECIMAL(12,8),
 V2 DECIMAL(12,8),
 V3 DECIMAL(12,8),
 V4 DECIMAL(12,8),
 V5 DECIMAL(12,8),
 V6 DECIMAL(12,8),
 V7 DECIMAL(12,8),
 V8 DECIMAL(12,8),
 V9 DECIMAL(12,8),
 V10 DECIMAL(12,8),
 V11 DECIMAL(12,8),
 V12 DECIMAL(12,8),
 V13 DECIMAL(12,8),
 V14 DECIMAL(12,8),
 V15 DECIMAL(12,8),
 V16 DECIMAL(12,8),
 V17 DECIMAL(12,8),
 V18 DECIMAL(12,8),
 V19 DECIMAL(12,8),
 V20 DECIMAL(12,8),
 V21 DECIMAL(12,8),
 V22 DECIMAL(12,8),
 V23 DECIMAL(12,8),
 V24 DECIMAL(12,8),
 V25 DECIMAL(12,8),
 V26 DECIMAL(12,8),
 V27 DECIMAL(12,8),
 V28 DECIMAL(12,8),
 Amount DECIMAL(14,8),
 Class INT unsigned
'''

# Define tables.
tables = ['labelled',
          'synthetic',
          'training',
          'validation',
          'test',
          'flagged',
          'unflagged'
          ]

# Name of database.
database = 'database/transactions.db'


# Create tables in sql database.
for table in tables:
    create_table(database=database, columns=columns, table=table)


filepath = 'data/creditcard.csv'
# Upload labelled data to labelled table in sql database.
csv_to_sql(filepath=filepath, database=database, table='labelled')
