"""."""


import numpy as np


def average_value(n_intervals, all_value):
    """."""
    average_value = all_value / n_intervals
    average_value = np.round(average_value, 2)

    return average_value
