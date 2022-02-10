"""."""

import numpy as np


def classify_transaction(model, value, threshold):
    """."""
    value = value.reshape(1, -1)
    probability = model.predict_proba(value)[:, 1]

    prediction = np.where(probability < threshold, 0, 1)

    return prediction[0]
