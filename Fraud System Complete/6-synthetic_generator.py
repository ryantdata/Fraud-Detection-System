"""Estimate density of data with gmm models for synthetic data generation."""


# packages
import pickle
import pandas as pd
from sklearn.mixture import GaussianMixture as GMM

# custom functions
from lib.sql_functions.sql_to_pd import sql_to_pd
from lib.training_functions.class_split import class_split
from lib.synth_functions.create_synth_data import create_synth_data
from lib.plot_functions.plot_compare_features import plot_compare_features
from lib.synth_functions.gmm_training import gmm_training
from lib.synth_functions.plot_bic_curve import plot_bic_curve


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

# split data by class label
drop_features = ['Transaction_id', 'Time', 'Class']
class_col = 'Class'
class0, class1 = class_split(data=data,
                             drop_features=drop_features,
                             class_col=class_col,
                             labl_a=0,
                             labl_b=1
                             )


# train class0 gmm -----------------------------------------------------------

# find good choice for n_components in gmm model.

# dataframe so it can be saved to parquet.
class0_bics = pd.DataFrame(columns=['bic'])

# load class0_aics from parquet file.
class0_bics = pd.read_parquet('pqdata\\class0_bics.pq', engine='pyarrow')

# plot n models and plot bic curve after each fitted model.
gmm_training(data=class0,
             bics=class0_bics,
             n=100,
             subset_name='class0',
             covariance_type='spherical'
             )
# BIC doesn't look like it will converge. Not surprising due to the amount of
# observations. Try 50 components and visually inspect similarity of
# synthetic data to real data.

# plot bic curve
plot_bic_curve(bics=class0_bics, subset_name='class0')

# save chosen model
gmm_class0 = GMM(50, covariance_type='full')
gmm_class0.fit(class0)
filename = 'pklmodels\\class0_gmm_model.sav'
pickle.dump(gmm_class0, open(filename, 'wb'))

# load chosen model from pkl file.
gmm_class0 = pickle.load(open('pklmodels\\class0_gmm_model.sav', 'rb'))


# create synthetic sample to compare with real data to assess model
synth0 = create_synth_data(class0, gmm_class0)


# create histograms for each feature to compare synthetic and real data
for i in range(len(class0.columns)):
    plot_compare_features(feature_a=class0.iloc[:, i],
                          feature_b=synth0.iloc[:, i],
                          title=f'Feature {class0.columns[i]} Distribution',
                          bins=80,
                          xlab=f'{class0.columns[i]}'
                          )
# plot mostly match the data, can't capture the double peaks however.
# good job overall.


# train class1 gmm -----------------------------------------------------------

# find good choice for n_components in gmm model.

# dataframe so it can be saved to parquet.
class1_bics = pd.DataFrame(columns=['bic'])

# load class0_aics from parquet file.
class1_bics = pd.read_parquet('pqdata\\class1_bics.pq', engine='pyarrow')

# plot n models and plot bic curve after each fitted model.
gmm_training(data=class1,
             bics=class1_bics,
             n=100,
             subset_name='class1',
             covariance_type='full'
             )
# good choice for n_components is 9

# plot bic curve
plot_bic_curve(bics=class1_bics, subset_name='class1')

# save chosen model
gmm_class1 = GMM(9, covariance_type='full')
gmm_class1.fit(class1)
filename = 'pklmodels\\class1_gmm_model.sav'
pickle.dump(gmm_class1, open(filename, 'wb'))

# load chosen model from pkl file.
gmm_class1 = pickle.load(open('pklmodels\\class1_gmm_model.sav', 'rb'))


# create synthetic sample to compare with real data to assess model
synth1 = create_synth_data(class1, gmm_class1)


# create histograms for each feature to compare synthetic and real data
for i in range(len(class1.columns)):
    plot_compare_features(feature_a=class1.iloc[:, i],
                          feature_b=synth1.iloc[:, i],
                          title=f'Feature {class1.columns[i]} Distribution',
                          bins=80,
                          xlab=f'{class1.columns[i]}'
                          )
# synth data matches real data very well in almost every feature.
