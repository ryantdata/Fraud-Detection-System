"""Train Logistic model."""


# packages
import numpy as np
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression

# custom functions
from lib.sql_functions.sql_to_pd import sql_to_pd
from lib.training_functions.best_threshold import best_threshold
from lib.training_functions.calc_clf_metrics import calc_clf_metrics


# import data
database = 'database/transactions.db'
table = 'training'
query = 'SELECT * FROM {}'.format(table)
train_data = sql_to_pd(database=database, query=query)

table = 'validation'
query = 'SELECT * FROM {}'.format(table)
validation_data = sql_to_pd(database=database, query=query)

# create training sets
x_train = train_data.drop(['Transaction_id', 'Time', 'Class'], axis=1)
x_val = validation_data.drop(['Transaction_id', 'Time', 'Class'], axis=1)
y_train = train_data['Class']
y_val = validation_data['Class']


# model selection ------------------------------------------------------------

# define parameter grid
param_grid = np.linspace(0.001, 1, 101)
# newton-cg low dimension/high obs count

# create metrics table
metrics = pd.DataFrame(columns=['gamma',
                                'recall',
                                'precision',
                                'best_threshold',
                                'confusion_matrix',
                                'hyperparameters'
                                ]
                       )

n_iter = len(param_grid)

for i in range(n_iter):

    # fit model
    model = LogisticRegression(solver='newton-cg', C=param_grid[i])
    model.fit(x_train, y_train)

    # calculate training set classification probabilities.
    probs_train = model.predict_proba(x_train)[:, 1]

    # find best threshold for training set.
    thresh = best_threshold(labels=y_train, probs=probs_train)

    # get results
    results = calc_clf_metrics(model=model,
                               x_data=x_val,
                               y_data=y_val,
                               thresh=thresh
                               )

    # save results
    index = len(metrics)
    metrics.loc[index] = [results[0],
                          results[1],
                          results[2],
                          results[3],
                          results[4],
                          param_grid[i]
                          ]
    metrics.to_parquet('pqdata\\logreg_metrics.pq')
    print(i)

# load results if kernel is reset
metrics = pd.read_parquet('pqdata\\logreg_metrics.pq', engine='pyarrow')


# chosen model ---------------------------------------------------------------

# C - 0.001
# gamma - 2.144
# recall - 0.788
# precision - 0.781
# best_threshold - 0.02
# conf_matrix - [71064    25    24    89]

# fit model
model = LogisticRegression(C=0.001, solver='newton-cg')
model.fit(x_train, y_train)

# save model
filename = 'pklmodels\\lr_model.sav'
pickle.dump(model, open(filename, 'wb'))

# load model
model = pickle.load(open('pklmodels\\lr_model.sav', 'rb'))
