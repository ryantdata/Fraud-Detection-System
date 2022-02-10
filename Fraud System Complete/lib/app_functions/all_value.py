"""."""


import numpy as np


def all_value(new_data, value):
    """."""
    new_value = new_data['Transaction_Value']
    new_value = value + new_value
    new_value = np.round(new_value, 2)

    return new_value
