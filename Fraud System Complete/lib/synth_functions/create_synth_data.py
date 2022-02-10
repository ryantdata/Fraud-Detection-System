"""."""


import pandas as pd


def create_synth_data(data, model):
    """."""
    synth = model.sample(len(data))[0]
    synth = pd.DataFrame(synth[:, 0:29])
    synth.columns = data.columns

    return synth
