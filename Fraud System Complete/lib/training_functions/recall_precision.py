"""Calculate precision and recall from a confusion matrix."""


def recall_precision(conf_matrix):
    """Calculate precision and recall from a confusion matrix.

    Parameters
    ----------
    conf_matrix: confusion matrix.

    Returns
    -------
    float recall: calculated recall.

    float precision: calculated precision.
    """
    tp = conf_matrix[1, 1]
    fp = conf_matrix[0, 1]
    fn = conf_matrix[1, 0]

    # coded this way to avoid weird errors.
    recall = 0
    precision = 0

    if (fn+tp) != 0:
        recall = tp / (fn+tp)

    if (tp+fp) != 0:
        precision = tp / (fp+tp)

    return recall, precision
