"""Estimate expected generalization error and conditional gen. error."""


# packages
import pandas as pd
import pickle
from xgboost import XGBClassifier

# custom functions
from lib.sql_functions.sql_to_pd import sql_to_pd
from lib.training_functions.bootstrap import bootstrap
from lib.training_functions.calc_clf_metrics import calc_clf_metrics
from lib.plot_functions.plot_bootstrap_dist import plot_bootstrap_dist

# import data
database = 'database/transactions.db'
table = 'training'
query = 'SELECT * FROM {}'.format(table)
train_data = sql_to_pd(database=database, query=query)

table = 'validation'
query = 'SELECT * FROM {}'.format(table)
validation_data = sql_to_pd(database=database, query=query)

table = 'test'
query = 'SELECT * FROM {}'.format(table)
test_data = sql_to_pd(database=database, query=query)

# create dataset to resample
data = pd.concat([train_data, validation_data, test_data], axis=0)


# calculate expected generalization error ------------------------------------

# bootstrapping

# load model
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

# create results dataframe
metrics = pd.DataFrame(columns=['recall', 'precision'])

# calculate precision and recall for N boostrap samples
drop_features = ['Transaction_id', 'Time']
class_col = 'Class'

# load results if kernel is reset
metrics = pd.read_parquet('pqdata\\bootstrap_results.pq', engine='pyarrow')

while True:

    # create bootstrap sample
    x_train, x_test, y_train, y_test = bootstrap(data=data,
                                                 test_size=0.5,
                                                 drop_features=drop_features,
                                                 class_col=class_col
                                                 )
    model.fit(x_train, y_train)

    # calculate results.
    results = calc_clf_metrics(model=model,
                               x_data=x_test,
                               y_data=y_test,
                               thresh=0.1
                               )

    index = len(metrics)
    print(index)

    # save metrics
    metrics.loc[index] = (results[1], results[2])
    metrics.to_parquet('pqdata\\bootstrap_results.pq')

# plot distribution of recall and precision
plot_bootstrap_dist(metrics['recall'], 'indianred', 'Recall')
plot_bootstrap_dist(metrics['precision'], 'steelblue', 'Precision')

# calculate mean and standard deviation.
metrics['recall'].mean()
metrics['precision'].mean()
metrics['recall'].std()
metrics['precision'].std()


# calculate conditional generalization error ---------------------------------

x_test2 = test_data.drop(['Transaction_id', 'Time', 'Class'], axis=1)
y_test2 = test_data['Class']
results = calc_clf_metrics(model=model,
                           x_data=x_test2,
                           y_data=y_test2,
                           thresh=0.1
                           )


# ready model for deployment -------------------------------------------------

# train chosen model on all data and save ready for deployment
x_data2 = data.drop(['Transaction_id', 'Time', 'Class'], axis=1)
y_data2 = data['Class']

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
model.fit(x_data2, y_data2)

# save model
filename = 'pklmodels\\deployed_xgb_model.sav'
pickle.dump(model, open(filename, 'wb'))

# load model
model = pickle.load(open('pklmodels\\deployed_xgb_model.sav', 'rb'))
