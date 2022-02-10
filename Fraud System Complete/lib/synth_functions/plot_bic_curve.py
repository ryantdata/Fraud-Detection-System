"""Plot BIC curve."""


import seaborn as sns
import matplotlib.pyplot as plt


def plot_bic_curve(bics, subset_name):
    """Plot BIC curve.

    Parameters
    ----------
    pd.DataFrame bics: contains columns 'bic' and 'index'.

    str subset_name: name of dataframe used to fit models.

    Returns
    -------
    NoneType None: None.
    """
    sns.lineplot(data=bics, x='index', y='bic')
    plt.title(f'BIC by Number of Components ({subset_name})')
    plt.xlabel('n_components')
    plt.ylabel('BIC')
    plt.show()

    return None
