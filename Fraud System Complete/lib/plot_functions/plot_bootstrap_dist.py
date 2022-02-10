"""Plot distribution of bootstrap estimate for metric."""


import seaborn as sns
import matplotlib.pyplot as plt


def plot_bootstrap_dist(data, color, name):
    """Plot distribution of bootstrap estimate for metric.

    Parameters
    ----------
    pd.Series data: vector of bootstrap estimates for a metric.

    str color: color of histogram.

    str name: name of metric to display in title. Capitalize.

    Returns
    -------
    NoneType None: None.
    """
    sns.histplot(
        data,
        kde=True,
        color=color
        ).set(title=f'Bootstrap {name} Distribution')
    plt.axvline(data.mean(), color='black')
    plt.show()

    return None
