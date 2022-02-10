"""Scale data with StandardScaler."""


from sklearn.preprocessing import StandardScaler
import pandas as pd


def scale(data, columns, cols):
    """Scale data with StandardScaler.

    Parameters
    ----------
    pd.DataFrame data: data to be scaled.

    list[str] columns: list of columns of the original data.

    list[str] cols: list of columns which should not be scaled.

    Returns
    -------
    pd.DataFrame scale: standard scaled data.
    """
    scaler = StandardScaler()
    scale = scaler.fit_transform(data)
    scale = pd.DataFrame(scale, columns=columns)
    data = data.reset_index(drop=True)

    for i in cols:
        scale[cols] = data[cols]

    return scale
