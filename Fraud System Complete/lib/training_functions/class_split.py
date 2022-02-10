"""Split dataset by class label."""


def class_split(data, drop_features, class_col, labl_a, labl_b):
    """Split dataset by class label.

    Parameters
    ----------
    pd.DataFrame data: dataset to split.

    list[str] drop_features: list of column names to remove from data.

    class_col: name of column containing class labels.

    str/int/float labl_a: name of first class label.

    str/int/float labl_b: name of second class label.

    Returns
    -------
    pd.DataFrame class_a: contains data corresponding to first class label.

    pd.DataFrame class_b: contains data corresponding to second class label.
    """
    class_a = data.loc[data[class_col] == labl_a]
    class_b = data.loc[data[class_col] == labl_b]
    class_a = class_a.drop(drop_features, axis=1)
    class_b = class_b.drop(drop_features, axis=1)

    return class_a, class_b
