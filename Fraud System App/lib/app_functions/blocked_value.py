"""."""


import numpy as np


def blocked_value(data, value):
    """."""
    new_value = data['Transaction_Value']
    value = value + new_value
    value = np.round(value, 2)

    return value
