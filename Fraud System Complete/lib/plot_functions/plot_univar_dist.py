"""Plot histogram of single feature for each class in binary class data."""


import seaborn as sns
import matplotlib.pyplot as plt


def plot_univar_dist(data,
                     column,
                     class_col,
                     labl_a,
                     labl_b,
                     bins,
                     log
                     ):
    """Plot histogram of single feature for each class in binary class data.

    Parameters
    ----------
    pd.DataFrame data: data from which to plot.

    str column: name of column feature to plot.

    str class_col: name of column containing class labels.

    str/int/float labl_a: label name for first class.

    str/int/float labl_b: label name for second class.

    int bins: number of bins in the histogram.

    bool log: if true, plots data on a log scale.

    Returns
    -------
    NoneType None: None.
    """
    class_a = data.loc[data[class_col] == labl_a]
    class_b = data.loc[data[class_col] == labl_b]
    fig, axs = plt.subplots(2, 1, sharex=True)

    if log:
        title = f'Log {column} Distribution'
        xlabel = f'Log {column}'
    else:
        title = f'{column} Distribution'
        xlabel = f'{column}'

    sns.histplot(data=class_a[column]+1,
                 kde=True,
                 log_scale=log,
                 ax=axs[0],
                 bins=bins,
                 color='green',
                 ).set(title=title)

    sns.histplot(data=class_b[column]+1,
                 kde=True,
                 log_scale=log,
                 ax=axs[1],
                 bins=bins,
                 color='red'
                 ).set(xlabel=xlabel)

    plt.show()

    return None
