"""Combine predictor and class data and covert to list of tuples."""


import numpy as np


def tuple_datasets(x_data, y_data):
    """Combine predictor and class data and covert to list of tuples.

    Parameters
    ----------
    pd.DataFrame x_data: dataframe of predictors.

    pd.Series y_data: series of class labels.

    Returns
    -------
    list[tuple] rows: combined x_data and y_data as list of tuples.
    """
    x = np.array(x_data)
    y = np.array(y_data)
    z = np.column_stack((x, y))
    rows = [tuple(j) for j in z]

    return rows
