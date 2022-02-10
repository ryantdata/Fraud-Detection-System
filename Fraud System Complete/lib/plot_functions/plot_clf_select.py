"""Plot recall and precision from set of trained classification models."""


import seaborn as sns
import matplotlib.pyplot as plt


def plot_clf_select(data):
    """Plot recall and precision from set of trained classification models.

    Parameters
    ----------
    pd.DataFrame data: dataframe with recall, precision and gamma columns.

    Returns
    -------
    NoneType None: None.
    """
    sns.scatterplot(data['recall'],
                    data['precision'],
                    hue=list(data['gamma']),
                    legend=False
                    ).set(title='Precision by Recall XGB models')
    plt.show()

    return None
