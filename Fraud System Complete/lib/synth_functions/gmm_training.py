"""Fit n GMM models to data and plot bic curve after each fitted model."""


import numpy as np
from sklearn.mixture import GaussianMixture as GMM

from lib.synth_functions.plot_bic_curve import plot_bic_curve


def gmm_training(data, bics, n, subset_name, covariance_type):
    """Fit n GMM models to data and plot bic curve after each fitted model.

    Parameters
    ----------
    pd.DataFrame data: data for gmm to estimate.

    list[float] bics: vector containing BIC values for each trained model.

    int n: number of GMM models to train. n_components increments 1 to n.

    str subset_name: name of dataframe.

    str covariance_type: sklearn GaussianMixture covariance_type.

    Returns
    -------
    NoneType None: None
    """
    n_components = np.linspace(1, n, n).astype(int)

    # define models.
    models = [GMM(m, covariance_type=covariance_type, random_state=0)
              for m in n_components]

    # create bic vector and calculate first entry if needed.
    if len(bics) == 0:
        bics.loc[0] = models[0].fit(data).bic(data)

    # calculate bic for each model until difference in bic is smaller than 5.
    for i in range(len(bics), len(models)):

        bics.loc[i] = models[i].fit(data).bic(data)
        bics['index'] = bics.index + 1
        bics.to_parquet(f'pqdata\\{subset_name}_bics.pq')

        # plot bic curve
        plot_bic_curve(bics=bics, subset_name=subset_name)

        print(i)

    return None
