"""Create train test split bootstrap from data."""


# packages
from sklearn.model_selection import train_test_split


def bootstrap(data, test_size, drop_features, class_col):
    """Create train test split bootstrap from data.

    Parameters
    ----------
    pd.DataFrame data: data to split into train and test sets.

    float test_size: proportion of data allocated to test set.

    list[str] drop_features: list of feature names to remove from data.

    str class_col: name of column containing class labels.

    Returns
    -------
    pd.DataFrame x_train: train set predictors.

    pd.DataFrame x_test: test set predictors.

    pd.DataFrame y_train: train set class labels.

    pd.DataFrame y_test: test set class labels.
    """
    bootstrap = data.sample(len(data), replace=True)
    X = bootstrap.drop(drop_features, axis=1)
    X = X.drop(class_col, axis=1)
    y = bootstrap[class_col]
    x_train, x_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        test_size=test_size)

    return x_train, x_test, y_train, y_test
