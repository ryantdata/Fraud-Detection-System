"""Model monitoring dashboard."""


# packages
import dash
from dash import html
from dash import Input
from dash import Output
from dash import State
from dash import dash_table
from dash import dcc
from dash import no_update
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np
import pickle
import pandas as pd

# custom functions
from lib.app_functions.new_transaction import new_transaction
from lib.app_functions.all_value import all_value
from lib.app_functions.average_value import average_value
from lib.app_functions.blocked_value import blocked_value
from lib.app_functions.upload_synth_data import upload_synth_data
from lib.app_functions.truncate_tables import truncate_tables


app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.SANDSTONE]
                )
server = app.server


# load deployed model.
clf_model = pickle.load(open('pklmodels\\deployed_xgb_model.sav',
                             'rb'
                             ))
generator_0 = pickle.load(open('pklmodels\\class0_gmm_model.sav',
                               'rb'
                               ))
generator_1 = pickle.load(open('pklmodels\\class1_gmm_model.sav',
                               'rb'
                               ))


# load static metrics.
model_metrics = pd.read_parquet('pqdata\\bootstrap_results.pq',
                                engine='pyarrow')


# columns that appear in live transaction table.
columns = [
           {'name': 'Time', 'id': 'Time'},
           {'name': 'Transaction_Value', 'id': 'Transaction_Value'},
           {'name': 'Prediction', 'id': 'Prediction'}
           ]


app.layout = dbc.Container([
    # Title
    dbc.Row([
        dbc.Col(
            html.H1(
                "Fraud Detection System Dashboard",
                className='text-center text-primary, mb-4'
                    )
                )
            ], style={'margin-top': '75px'}),

    # System Controls
    dbc.Row(
        dbc.Col(
            html.H3(
                "System Controls",
                className='text-primary, mb-2',
                style={"margin-left": "8px"}
                    )
                )
            ),

    # Buttons
    dbc.Row([
        dbc.Col([
                dbc.Button(
                    'Stop',
                    id='stop',
                    color='light',
                    className='mb-5',
                    style={"margin-left": "8px"}
                           ),

                dbc.Button(
                    'Start',
                    id='start',
                    color='secondary',
                    className='mb-5',
                    style={"margin-left": "8px"}
                    ),

                dbc.Button(
                    'Reset',
                    id='restart',
                    color='dark',
                    className='mb-5',
                    style={"margin-left": "8px"}
                )],
                width={'size': 3},
                ),
            ], style={'border-bottom-style': 'solid',
                      'border-bottom-width': '5px'}),

    # Model Tracking Metrics
    dbc.Row(
        dbc.Col(
            html.H1(
                "Model Tracking Metrics",
                className='text-center text-primary, mb-4'
                    )
                ), style={'margin-top': '50px',
                          'margin-bottom': '40px'
                          }
            ),

    # Transaction trackers
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4(
                    children='Number of Transactions',
                    style={'text-align': 'center',
                           'height': '40px'
                           }
                        ),
                html.P(
                    id='count',
                    children=int(),
                    style={'font-weight': 'bold',
                           'font-size': '72px',
                           'text-align': 'center'
                           }
                       )
                      ], style={'height': '200px'}
                     )
                ]),

        dbc.Col([
            html.Div([
                html.H4(
                    children='Total Value of Transactions',
                    style={'text-align': 'center',
                           'height': '64px'
                           }
                        ),
                html.Div([
                     html.Span(
                         children='£',
                               ),
                     html.Span(
                         id='all_value',
                         children=float(),
                               )
                     ],
                    style={'font-weight': 'bold',
                           'font-size': '48px',
                           'text-align': 'center',
                           'height': '150px',
                           'margin-bottom': '51px'
                           }
                         ),
                      ], style={'height': '200px'}
                     )
                ]),

        dbc.Col([
            html.Div([
                html.H4(
                    children='Average Value of Transactions',
                    style={'text-align': 'center',
                           'height': '64px'
                           }
                        ),
                html.Div([
                    html.Span(
                              children='£',
                              ),
                    html.Span(
                              id='average_value',
                              children=float()
                              )
                         ],
                         style={'font-weight': 'bold',
                                'font-size': '48px',
                                'text-align': 'center'
                                }
                         )
                      ], style={'height': '200px'}
                     )
                ]),
            ], style={'margin-top': '50px'}),

    # Passed transactions graphs
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H3(
                    children='Distribution of Unblocked Transaction Values',
                    style={'text-align': 'center',
                           'height': '40px',
                           'margin-top': '50px'
                           }
                        ),
                dcc.Graph(
                    id='figure_all_value',
                    figure={},
                    style={'margin-bottom': '50px'}
                          ),
                    ])
                ),

        dbc.Col(
            html.Div([
                html.H3(
                    children='Log-Scale of Unblocked Transaction Values',
                    style={'text-align': 'center',
                           'height': '40px',
                           'margin-top': '50px'
                           }
                        ),
                dcc.Graph(
                    id='figure_all_log',
                    figure={},
                    style={'margin-bottom': '50px'}
                          ),
                    ])
                ),
            ],  style={'border-bottom-style': 'solid',
                       'border-top-style': 'solid',
                       'border-bottom-width': '2px',
                       'border-top-width': '2px'}),

    # Blocked transactions tracker
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4(
                    children='Number of Blocked Transactions',
                    style={'text-align': 'center',
                           'height': '40px'
                           }
                        ),
                html.P(
                    id='blocked_count',
                    children=int(),
                    style={'font-weight': 'bold',
                           'font-size': '72px',
                           'text-align': 'center'
                           }
                       )
                      ], style={'height': '200px'}
                     ),
                ]),

        dbc.Col([
            html.Div([
                html.H4(
                    children='Total Value of Blocked Transactions',
                    style={'text-align': 'center',
                           'height': '64px'
                           }
                        ),
                html.Div([
                    html.Span(
                        children='£'
                              ),
                    html.Span(
                        id='blocked_value',
                        children=float()
                              )
                         ],
                         style={'font-weight': 'bold',
                                'font-size': '48px',
                                'text-align': 'center'
                                }
                         )
                      ], style={'height': '200px'}
                     ),
                ]),

        dbc.Col([
            html.Div([
                html.H4(
                    children='Average Value of Blocked Transactions',
                    style={'text-align': 'center',
                           'height': '64px'
                           }
                        ),
                html.Div([
                    html.Span(
                        children='£'
                              ),
                    html.Span(
                          id='average_blocked_value',
                          children=float()
                              )
                         ],
                         style={'font-weight': 'bold',
                                'font-size': '48px',
                                'text-align': 'center'
                                }
                         )
                      ], style={'height': '200px'}
                     ),
                ]),
            ], style={'margin-top': '50px'}),

    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4(
                    children='Percentage of Transactions '
                             'Blocked',
                    style={'text-align': 'center',
                           'height': '64px'
                           }
                        ),
                html.Div([
                    html.Span(
                        id='block_rate',
                        children=float()
                              ),
                    html.Span(
                        children='%'
                              )
                         ],
                         style={'font-weight': 'bold',
                                'font-size': '48px',
                                'text-align': 'center'
                                }
                         )
                      ], style={'height': '200px'}
                     ),
                ]),

        dbc.Col([
            html.Div([
                html.H4(
                    children='Value of Last Blocked Transaction',
                    style={'text-align': 'center',
                           'height': '64px'
                           }
                        ),
                html.Div([
                    html.Span(
                        children='£'
                              ),
                    html.Span(
                        id='last_blocked_value',
                        children=float()
                              )
                         ],
                         style={'font-weight': 'bold',
                                'font-size': '48px',
                                'text-align': 'center'
                                }
                         )
                      ], style={'height': '200px'}
                     )
                ]),
            ], style={'margin-top': '50px'}),

    # Blocked transactions graphs
    dbc.Row([
        dbc.Col([
            html.H3(
                children='Distribution of Blocked Transaction Values',
                style={'text-align': 'center',
                       'height': '40px',
                       'margin-top': '50px'
                       }
                    ),
            dcc.Graph(
                id='figure_blocked_value',
                figure={},
                style={'margin-bottom': '50px'}
                      ),
               ]),

        dbc.Col([
            html.H3(
                children='Log-Scale of Blocked Transaction Values',
                style={'text-align': 'center',
                       'height': '40px',
                       'margin-top': '50px'
                       }
                    ),
            dcc.Graph(
                id='figure_blocked_log',
                figure={},
                style={'margin-bottom': '50px'}
                      )
                ]),
            ], style={'border-bottom-style': 'solid',
                      'border-top-style': 'solid',
                      'border-bottom-width': '5px',
                      'border-top-width': '2px'}),

    # Static model metrics title
    dbc.Row(
        dbc.Col(
            html.H1(
                "Static Model Metrics",
                className='text-center text-primary, mb-4'
                    )
                ), style={'margin-top': '50px',
                          'margin-bottom': '40px'
                          }
            ),

    # Expected recall and precision
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4(
                    children='Estimate of Expected Recall',
                    style={'text-align': 'center',
                           'height': '64px'
                           }
                        ),
                html.P(
                    children='87.6%',
                    style={'font-weight': 'bold',
                           'font-size': '48px',
                           'text-align': 'center'
                           }
                       )
                      ], style={'height': '200px'}
                     ),

            html.Div([
                html.H4(
                    children='Estimate of Expected Precision',
                    style={'text-align': 'center',
                           'height': '64px'
                           }
                        ),
                html.P(
                    children='93.3%',
                    style={'font-weight': 'bold',
                           'font-size': '48px',
                           'text-align': 'center'
                           }
                       )
                      ], style={'height': '200px'}
                     ),
                ]),

        dbc.Col([
            html.Div([
                html.H4(
                    children='Standard Deviation of Recall',
                    style={'text-align': 'center',
                           'height': '64px'
                           }
                        ),
                html.P(
                    children='2.41%',
                    style={'font-weight': 'bold',
                           'font-size': '48px',
                           'text-align': 'center'
                           }
                       )
                      ], style={'height': '200px'}
                     ),

            html.Div([
                html.H4(
                    children='Standard Deviation of Precision',
                    style={'text-align': 'center',
                           'height': '64px'
                           }
                        ),
                html.P(
                    children='2.17%',
                    style={'font-weight': 'bold',
                           'font-size': '48px',
                           'text-align': 'center'
                           }
                       )
                      ], style={'height': '200px'}
                     ),
                ]),

        dbc.Col([
            html.Div([
                html.H4(
                    children='95% Confidence Interval For Recall',
                    style={'text-align': 'center',
                           'height': '64px'
                           }
                        ),
                html.P(
                    children='[82.8%, 92.4%]',
                    style={'font-weight': 'bold',
                           'font-size': '32px',
                           'text-align': 'center'
                           }
                       )
                      ], style={'height': '200px'}
                     ),

            html.Div([
                html.H4(
                    children='95% Confidence Interval For Precision',
                    style={'text-align': 'center',
                           'height': '64px'
                           }
                        ),
                html.P(
                    children='[89.0%, 97.6%]',
                    style={'font-weight': 'bold',
                           'font-size': '32px',
                           'text-align': 'center'
                           }
                       )
                      ], style={'height': '200px'}
                     )
                ]),
            ]),

    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4(
                    children='Estimate of Expected Block Rate',
                    style={'text-align': 'center',
                           'height': '64px'
                           }
                        ),
                html.P(
                    children='0.217%',
                    style={'font-weight': 'bold',
                           'font-size': '48px',
                           'text-align': 'center'
                           }
                       )
                      ], style={'height': '200px'}
                     ),
                ]),

        dbc.Col([
            html.Div([
                html.H4(
                    children='Estimate of Expected Miss Rate',
                    style={'text-align': 'center',
                           'height': '64px'
                           }
                        ),
                html.P(
                    children='0.0515%',
                    style={'font-weight': 'bold',
                           'font-size': '48px',
                           'text-align': 'center'
                           }
                       )
                      ], style={'height': '200px'}
                     )
                ])
            ]),

    # Recall and precision graphs
    dbc.Row([
        dbc.Col([
            html.H3(
                children='Distribution of Recall Estimates',
                style={'text-align': 'center',
                       'height': '40px',
                       'margin-top': '50px'
                       }
                    ),
            dcc.Graph(
                id='figure_recall',
                figure={},
                style={'margin-bottom': '50px'}
                      ),
               ]),

        dbc.Col([
            html.H3(
                children='Distribution of Precision Estimates',
                style={'text-align': 'center',
                       'height': '40px',
                       'margin-top': '50px'
                       }
                    ),
            dcc.Graph(
                id='figure_precision',
                figure={},
                style={'margin-bottom': '50px'}
                      )
                ]),
            ], style={'border-bottom-style': 'solid',
                      'border-top-style': 'solid',
                      'border-bottom-width': '5px',
                      'border-top-width': '2px'}),

    # Title
    dbc.Row([
        dbc.Col(
            html.H1(
                "New Transactions Feed",
                className='text-center text-primary, mb-4'
                    )
                )
            ], style={'margin-top': '50px'}),

    # Transactions table
    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
                id='table',
                data=[],
                columns=[],
                style_as_list_view=True,
                style_cell={'padding': '5px'},
                style_header={
                              'backgroundColor': 'white',
                              'fontWeight': 'bold'
                              },
                                 ), width={'size': 12}
                ),
            ], style={'margin-top': '50px',
                      'margin-bottom': '150px'}),

    dcc.Interval(
        id='interval',
        interval=1000,
        n_intervals=0
                 ),

    dcc.Store(
        id='new_sample',
        storage_type='memory',
        data=[]
              ),

    dcc.Store(
        id='is_stop',
        storage_type='memory',
        data=[]
              ),

    dcc.Store(
        id='is_restart',
        storage_type='memory',
        data=[]
              ),

    dcc.Store(
        id='figure_all_data',
        storage_type='memory',
        data=[]
              ),

    dcc.Store(
        id='figure_blocked_data',
        storage_type='memory',
        data=[]
              )
])


# System controls
@app.callback(
    [
     Output('interval', 'n_intervals'),
     Output('interval', 'disabled'),
     Output('is_stop', 'data'),
     Output('is_restart', 'data')
     ],
    [
     Input('start', 'n_clicks'),
     Input('stop', 'n_clicks'),
     Input('restart', 'n_clicks')
     ],
    [
     State('interval', 'n_intervals')
     ]
)
def controls(stop, start, restart, current):
    """."""
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'restart' in changed_id:
        return [0, True, False, True]

    elif 'stop' in changed_id:
        return [current, True, True, False]

    elif 'start' in changed_id:
        return [current, False, False, False]

    return [current, False, False, False]


# create new synthetic data and update live transaction table.
@app.callback(
    [
     Output('table', 'data'),
     Output('table', 'columns'),
     Output('count', 'children'),
     Output('new_sample', 'data')
     ],
    [
     Input('interval', 'n_intervals'),
     Input('is_stop', 'data'),
     Input('is_restart', 'data')
     ],
    [
     State('table', 'data')
    ]
)
def update_tables(n_intervals, is_stop, is_restart, data):
    """."""
    if is_stop:
        raise PreventUpdate

    if is_restart:
        data = []
        count = 0
        truncate_tables()

        return [data, columns, count, data]

    if n_intervals == 0:
        data = []

    if len(data) >= 10:
        data = data[:-1]

    new_data, new_sample, prediction = new_transaction(model=clf_model,
                                                       generator_0=generator_0,
                                                       generator_1=generator_1
                                                       )

    new_data['Prediction'] = prediction
    data.insert(0, new_data)
    count = n_intervals + 1

    upload_synth_data(new_sample, prediction)

    return [data, columns, count, new_data]


# update dynamic metrics.
@app.callback(
              [
               Output('all_value', 'children'),
               Output('average_value', 'children'),
               Output('blocked_value', 'children'),
               Output('blocked_count', 'children'),
               Output('block_rate', 'children'),
               Output('average_blocked_value', 'children'),
               Output('last_blocked_value', 'children')
               ],
              [
               Input('new_sample', 'data'),
               State('is_stop', 'data'),
               State('is_restart', 'data')
               ],
              [
               State('count', 'children'),
               State('all_value', 'children'),
               State('blocked_value', 'children'),
               State('blocked_count', 'children'),
               State('last_blocked_value', 'children')
               ]
)
def updata__(new_data,
             is_stop,
             is_restart,
             count,
             all_val,
             blocked_val,
             blocked_count,
             last_blocked_val,
             ):
    """."""
    if is_stop:
        raise PreventUpdate

    if is_restart:

        all_val = 0
        average_val = 0
        block_rate = 0
        blocked_val = 0
        blocked_count = 0
        average_blocked_val = 0
        last_blocked_val = 0

        return [all_val,
                average_val,
                blocked_val,
                blocked_count,
                block_rate,
                average_blocked_val,
                last_blocked_val
                ]

    all_val = all_value(new_data, all_val)
    average_val = average_value(count, all_val)

    if new_data['Prediction'] == 1:
        blocked_count = blocked_count + 1
        blocked_val = blocked_value(new_data, blocked_val)
        last_blocked_val = np.round(new_data['Transaction_Value'], 2)

    block_rate = np.round(100*blocked_count / count, 2)

    if blocked_count > 0:
        average_blocked_val = np.round(blocked_val / blocked_count, 2)
    else:
        average_blocked_val = 0

    return [all_val,
            average_val,
            blocked_val,
            blocked_count,
            block_rate,
            average_blocked_val,
            last_blocked_val
            ]


# update unblocked transactions graphs.
@app.callback(
              [
               Output('figure_all_data', 'data'),
               Output('figure_all_value', 'figure'),
               Output('figure_all_log', 'figure')
               ],
              [
               Input('new_sample', 'data'),
               Input('is_stop', 'data'),
               Input('is_restart', 'data')
               ],
              [
               State('figure_all_data', 'data'),
               State('interval', 'n_intervals')
               ]
)
def all_transactions_distplot(new_data,
                              is_stop,
                              is_restart,
                              figure_data,
                              n_intervals
                              ):
    """."""
    if is_stop:
        raise PreventUpdate

    if is_restart:
        figure_data = []
        figure = {}
        figure_log = {}

        return[figure_data, figure, figure_log]

    if n_intervals == 0:
        figure_data = []
        figure = {}
        figure_log = {}

    if new_data['Prediction'] == 0:
        figure_data.insert(0, new_data)

    if len(figure_data) < 10:
        return [figure_data, no_update, no_update]

    figure_data = pd.DataFrame(figure_data)
    figure = px.histogram(
                          figure_data['Transaction_Value'],
                          template="simple_white",
                          color_discrete_sequence=['seagreen']
                          )
    figure.update_xaxes(tickfont_size=20, titlefont_size=25)
    figure.update_yaxes(tickfont_size=20, titlefont_size=25)
    figure.update_layout(showlegend=False)

    figure_log = px.histogram(
                          np.log(figure_data['Transaction_Value']),
                          template="simple_white",
                          color_discrete_sequence=['seagreen']
                          )
    figure_log.update_xaxes(tickfont_size=20, titlefont_size=25)
    figure_log.update_yaxes(tickfont_size=20, titlefont_size=25)
    figure_log.update_layout(showlegend=False)

    return [figure_data.to_dict('records'), figure, figure_log]


# update blocked transactions graphs.
@app.callback(
              [
               Output('figure_blocked_data', 'data'),
               Output('figure_blocked_value', 'figure'),
               Output('figure_blocked_log', 'figure')
               ],
              [
               Input('new_sample', 'data'),
               Input('is_stop', 'data'),
               Input('is_restart', 'data')
               ],
              [
               State('figure_blocked_data', 'data'),
               State('interval', 'n_intervals')
               ]
)
def blocked_transactions_distplot(new_data,
                                  is_stop,
                                  is_restart,
                                  figure_data,
                                  n_intervals
                                  ):
    """."""
    if is_stop:
        raise PreventUpdate

    if is_restart:
        figure_data = []
        figure_blocked = {}
        figure_blocked_log = {}

        return [figure_data, figure_blocked, figure_blocked_log]

    if n_intervals == 0:
        figure_data = []
        figure_blocked = {}
        figure_blocked_log = {}

    if new_data['Prediction'] == 1:
        figure_data.insert(0, new_data)

    if len(figure_data) < 10:
        return [figure_data, no_update, no_update]

    figure_data = pd.DataFrame(figure_data)
    figure_blocked = px.histogram(
        figure_data['Transaction_Value'],
        template="simple_white",
        color_discrete_sequence=['indianred']
        )
    figure_blocked.update_xaxes(tickfont_size=20, titlefont_size=25)
    figure_blocked.update_yaxes(tickfont_size=20, titlefont_size=25)
    figure_blocked.update_layout(showlegend=False)

    figure_blocked_log = px.histogram(
        np.log(figure_data['Transaction_Value']),
        template="simple_white",
        color_discrete_sequence=['indianred']
        )
    figure_blocked_log.update_xaxes(tickfont_size=20, titlefont_size=25)
    figure_blocked_log.update_yaxes(tickfont_size=20, titlefont_size=25)
    figure_blocked_log.update_layout(showlegend=False)

    return [figure_data.to_dict('records'),
            figure_blocked,
            figure_blocked_log
            ]


# create static metrics graph.
@app.callback(
              [
               Output('figure_recall', 'figure'),
               Output('figure_precision', 'figure')
               ],
              [
               Input('interval', 'n_intervals')
               ]
)
def recall_precision_plot(n_intervals):
    """."""
    figure_recall = px.histogram(
        model_metrics['recall'],
        template="simple_white",
        color_discrete_sequence=['goldenrod'],
        x='recall'
        )
    figure_recall.update_xaxes(tickfont_size=20, titlefont_size=25)
    figure_recall.update_yaxes(tickfont_size=20, titlefont_size=25)
    figure_recall.update_layout(showlegend=False)

    figure_precision = px.histogram(
        model_metrics['precision'],
        template="simple_white",
        color_discrete_sequence=['silver'],
        x='precision'
        )
    figure_precision.update_xaxes(tickfont_size=20, titlefont_size=25)
    figure_precision.update_yaxes(tickfont_size=20, titlefont_size=25)
    figure_precision.update_layout(showlegend=False)

    return [figure_recall, figure_precision]


if __name__ == "__main__":
    app.run_server(debug=False)
