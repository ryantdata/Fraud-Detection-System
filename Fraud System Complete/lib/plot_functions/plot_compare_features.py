"""Plot histograms of two features to compare them."""


import seaborn as sns
import matplotlib.pyplot as plt


def plot_compare_features(feature_a, feature_b, title, bins, xlab):
    """Plot histograms of two features to compare them.

    Parameters
    ----------
    pd.Series feature_a: Vector of feature values.

    pd.Series feature_b: Vector of feature values.

    str title: Title of plot.

    int bins: number of histogram bins.

    str xlab: name of feature.

    Returns
    -------
    NoneType None: None.
    """
    fig, axs = plt.subplots(2, 1, sharex=True)
    sns.histplot(data=feature_a,
                 kde=True,
                 ax=axs[0],
                 bins=bins,
                 color='green',
                 ).set(title=title)
    sns.set(font_scale=1.5)

    sns.histplot(data=feature_b,
                 kde=True,
                 ax=axs[1],
                 bins=bins,
                 color='red'
                 ).set(xlabel=xlab)
    sns.set(font_scale=1.5)
    plt.show()

    return None
