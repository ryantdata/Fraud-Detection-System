"""Train XGB model."""


# packages
import pandas as pd
import numpy as np
import pickle
from xgboost import XGBClassifier

# custom functions
from lib.sql_functions.sql_to_pd import sql_to_pd
from lib.training_functions.best_threshold import best_threshold
from lib.training_functions.calc_clf_metrics import calc_clf_metrics
from lib.training_functions.define_xgb_model import define_xgb_model
from lib.plot_functions.plot_clf_select import plot_clf_select

# import data
database = 'database/transactions.db'
table = 'training'
query = 'SELECT * FROM {}'.format(table)
train_data = sql_to_pd(database=database, query=query)

table = 'validation'
query = 'SELECT * FROM {}'.format(table)
validation_data = sql_to_pd(database=database, query=query)

# create training sets.
x_train = train_data.drop(['Transaction_id', 'Time', 'Class'], axis=1)
x_val = validation_data.drop(['Transaction_id', 'Time', 'Class'], axis=1)
y_train = train_data['Class']
y_val = validation_data['Class']


# model selection ------------------------------------------------------------

# define parameter space
learning_rate = np.linspace(0.01, 0.3, 101)
min_split_loss = np.linspace(0, 20, 201)
max_depth = np.linspace(2, 15, 14).astype(int)
min_child_weight = np.linspace(1, 20, 20).astype(int)
max_delta_step = np.linspace(0, 20, 201)
reg_lambda = np.linspace(0, 20, 201)
reg_alpha = np.linspace(0, 20, 201)
n_estimators = np.linspace(25, 400, 51).astype(int)

# create metrics table
metrics = pd.DataFrame(columns=['gamma',
                                'recall',
                                'precision',
                                'best_threshold',
                                'confusion_matrix',
                                'hyperparameters'
                                ]
                       )

# randomized grid search, saves results of each loop, can stop anytime without
# losing progress.
while True:

    # fit model
    model, params = define_xgb_model(learning_rate=learning_rate,
                                     min_split_loss=min_split_loss,
                                     max_depth=max_depth,
                                     min_child_weight=min_child_weight,
                                     max_delta_step=max_delta_step,
                                     reg_lambda=reg_lambda,
                                     reg_alpha=reg_alpha,
                                     n_estimators=n_estimators
                                     )
    model.fit(x_train,
              y_train,
              eval_metric='logloss',
              verbose=False
              )

    # calculate classification probabilities for training set.
    probs_train = model.predict_proba(x_train)[:, 1]

    # find best threshold for training set.
    thresh = best_threshold(labels=y_train, probs=probs_train)

    # calculate results
    results = calc_clf_metrics(model=model,
                               x_data=x_val,
                               y_data=y_val,
                               thresh=thresh
                               )

    # save results
    index = len(metrics)
    print(index)
    metrics.loc[index] = [results[0],
                          results[1],
                          results[2],
                          results[3],
                          results[4],
                          (
                           params[0],
                           params[1],
                           params[2],
                           params[3],
                           params[4],
                           params[5],
                           params[6],
                           params[7],
                           )
                          ]
    metrics.to_parquet('pqdata\\xgb_metrics.pq')

# load results if kernel is reset
metrics = pd.read_parquet('pqdata\\xgb_metrics.pq', engine='pyarrow')

# plot recall / precision scatterplot
plot_clf_select(data=metrics)


# chosen model ---------------------------------------------------------------

# gamma - 2.242
# recall - 0.814
# precision - 0.8
# best_threshold - 0.1
# confusion_matrix - [71066    23    21   92]
# parameters - (0.2565, 0.0, 9, 9, 1.7, 19.0, 0.1, 325)

# fit model
model = XGBClassifier(learning_rate=0.2565,
                      min_split_loss=0,
                      max_depth=9,
                      min_child_weight=9,
                      max_delta_step=1.7,
                      reg_lambda=19,
                      reg_alpha=0.1,
                      n_estimators=325,
                      use_label_encoder=False,
                      eval_metric='logloss',
                      )
model.fit(x_train, y_train)

# save model
filename = 'pklmodels\\xgb_model.sav'
pickle.dump(model, open(filename, 'wb'))

# load model
model = pickle.load(open('pklmodels\\xgb_model.sav', 'rb'))
