"""Calculate performance metrics for classification model evaluation."""


# packages
import numpy as np
from sklearn.metrics import confusion_matrix

# custom functions
from lib.training_functions.recall_precision import recall_precision


def calc_clf_metrics(model, x_data, y_data, thresh):
    """Calculate performance metrics for classification model evaluation.

    Parameters
    ----------
    model: model to test.

    pd.DataFrame x_data: validation data predictors.

    pd.Series y_data: validation data class labels.

    float thresh: classification threshold.

    Returns
    -------
    float gamma: modified Youden's Index (YI= -1 + Rec + Pre).

    float recall: recall.

    float precision: precision.

    float best_thresh: best threshold found by maximising gamma.

    array conf_matrix: confusion matrix.
    """
    probs = model.predict_proba(x_data)[:, 1]
    preds = np.where(probs < thresh, 0, 1)
    conf_matrix = confusion_matrix(y_data, preds)

    recall, precision = recall_precision(conf_matrix)
    gamma = -1 + 3*recall + precision
    conf_matrix = np.reshape(conf_matrix, 4)

    return gamma, recall, precision, thresh, conf_matrix
