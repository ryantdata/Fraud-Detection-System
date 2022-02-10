"""Plot number of observations in each class for binary classification data."""


import seaborn as sns
import matplotlib.pyplot as plt


def plot_class_dist(data, column, labl_a, labl_b):
    """Plot number of obs in each class for binary classification data.

    Parameters
    ----------
    pd.DataFrame data: data containing class labels.

    str column: name of column containing class labels.

    str/int/float labl_a: label name for first class.

    str/int/float labl_b: label name for second class.

    Returns
    -------
    NoneType None: None.
    """
    class_a = len(data.loc[data[column] == labl_a])
    class_b = len(data.loc[data[column] == labl_b])

    sns.set_theme(style='white', palette=None)
    sns.barplot(x=[0, 1], y=[class_a, class_b], color='skyblue')
    plt.xlabel('Class')
    plt.ylabel('Number of Records')
    plt.title('Number of Records in each Class')

    return None
