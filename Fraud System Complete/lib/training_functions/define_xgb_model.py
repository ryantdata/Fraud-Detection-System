"""Define XGB model with random set of parameters from a defined range."""


import random
from xgboost import XGBClassifier


def define_xgb_model(learning_rate,
                     min_split_loss,
                     max_depth,
                     min_child_weight,
                     max_delta_step,
                     reg_lambda,
                     reg_alpha,
                     n_estimators
                     ):
    """Define XGB model with random set of parameters from a defined range.

    Parameters
    ----------
    float learning_rate: xgb learning rate.

    float min_split_loss: xgb min_split_loss.

    int max_depth: xgb max_depth.

    int min_child_weight: xgb min_child_weight.

    float reg_lambda: xgb reg_lambda.

    float reg_alpha: xgb reg_alpha.

    int n_estimators: xgb n_estimators.

    Returns
    -------
    model: model defined with a set of random parameters.

    tuple[int/float] params: random set of parameters used in model.
    """
    params = (random.choice(learning_rate),
              random.choice(min_split_loss),
              random.choice(max_depth),
              random.choice(min_child_weight),
              random.choice(max_delta_step),
              random.choice(reg_lambda),
              random.choice(reg_alpha),
              random.choice(n_estimators)
              )

    model = XGBClassifier(learning_rate=params[0],
                          min_split_loss=params[1],
                          max_depth=params[2],
                          min_child_weight=params[3],
                          max_delta_step=params[4],
                          reg_lambda=params[5],
                          reg_alpha=params[6],
                          use_label_encoder=False,
                          n_estimators=params[7],
                          seed=0
                          )

    return model, params
