"""Plot a heatmap of the upper right triangle of a correlation matrix."""


import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def plot_corr(data):
    """Plot a heatmap of the upper right triangle of a correlation matrix.

    Parameters
    ----------
    pd.DataFrame data: numerical data to plot.

    Returns
    -------
    NoneType None: None.
    """
    sns.set_theme(style='white', palette=None)

    try:
        data = data.astype(float)
    except TypeError:
        print('Make sure all values in dataframe can be converted to float!')

    correlation = data.corr()

    # Hides lower triangle of correlation matrix. Note: np.triu hides upper.
    mask = np.tril(np.ones_like(correlation, dtype=bool))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    graphics = sns.heatmap(correlation,
                           cmap=cmap,
                           mask=mask,
                           vmax=1,
                           vmin=-1,
                           center=0,
                           square=True,
                           linewidths=.5,
                           cbar_kws={'shrink': .5}
                           )

    for _, spine in graphics.spines.items():
        spine.set_visible(True)

    plt.xlabel('Features')
    plt.ylabel('Features')
    plt.title('Correlation Matrix')

    return None
