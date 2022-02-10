"""."""


import random
import numpy as np

from lib.app_functions.new_sample import new_sample


def new_transaction(model, generator_0, generator_1):
    """."""
    x = random.randint(0, 4)
    if x == 1:
        sample, data = new_sample(generator_1, x)
    else:
        sample, data = new_sample(generator_0, x)

    probability = model.predict_proba(sample)[:, 1]
    prediction = np.where(probability < 0.1, 0, 1)

    return data, sample[0], prediction[0]
