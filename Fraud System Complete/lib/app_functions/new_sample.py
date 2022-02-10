"""Generate synthetic data sample."""

import datetime as dt
import numpy as np


def new_sample(generator, x):
    """Generate synthetic data sample.

    Parameters
    ----------
    model generator: model used to generate sample.

    Returns
    -------
    np.ndarray sample: returns array of values for a single observation.

    dict data: returns formatted information for dashboard.
    """
    sample = generator.sample(1)[0]

    if x == 1:
        value = float(sample[:, 28])
        value = value*2.214 + 2.821
        value = np.exp(value) - 1
    else:
        value = float(sample[:, 28])
        value = value*1.655 + 3.153
        value = np.exp(value) - 1

    data = {'Time': dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Transaction_Value': abs(value),
            'Prediction': 0
            }

    return sample, data
