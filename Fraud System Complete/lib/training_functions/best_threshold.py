"""Calculate classification threshold value by maximising gamma."""


# packages
import numpy as np
from sklearn.metrics import confusion_matrix

# custom functions
from lib.training_functions.recall_precision import recall_precision


def best_threshold(labels, probs):
    """Calculate classification threshold value by maximising gamma.

    Parameters
    ----------
    pd.Series labels: real class labels.

    np.array probs: array of classification probabilities.

    Returns
    -------
    float best_thresh: best classification threshold value for the model.
    """
    gamma_values = []
    thresh = np.linspace(0.01, 0.99, 99)

    for i in thresh:
        preds = np.where(probs < i, 0, 1)
        conf_matrix = confusion_matrix(labels, preds)
        recall, precision = recall_precision(conf_matrix)

        gamma = -1 + 3*recall + precision
        gamma_values.append(gamma)

    max_index = gamma_values.index(max(gamma_values))
    best_thresh = thresh[max_index]

    return best_thresh
