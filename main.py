import pandas as pd
import plotly.express as px  # (version 4.7.0)

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import textwrap

app = dash.Dash(__name__)

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
lett = pd.read_csv(
    "https://vgprojectwarwick.s3-eu-west-1.amazonaws.com/letters/formatted_letter_data_2.csv")
art = pd.read_csv(
    "https://vgprojectwarwick.s3-eu-west-1.amazonaws.com/new+art/eatr.csv")
art_columns = art.columns[1:10]
# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    html.H1("Vincent van Gogh Exploror",
            style={'text-align': 'center'}),
    html.Br(),
    html.H2("Letters", style={"margin": "0 5px"}),
    html.Br(),
    html.Label([
        "Select X axis",
        dcc.Dropdown(id="select_x",
                     options=[
                         {"label": "Valence",
                          "value": 'valence'},
                         {"label": "Arousal",
                          "value": 'arousal'},
                         {"label": "Dominance",
                          "value": 'dominance'},
                         {"label": "Concreteness",
                          "value": 'concreteness'},
                         {"label": "Date", "value": 'date'}],
                     multi=False,
                     value='date',
                     style={'width': "100%", "margin-top": "0.5rem"}
                     ), ], style={"margin": "5px"}),
    html.Br(),
    html.Label([
        "Select Y axis",
        dcc.Dropdown(
            id="select_y",
            options=[
                {"label": "Valence",
                 "value": 'valence'},
                {"label": "Arousal",
                 "value": 'arousal'},
                {"label": "Dominance",
                 "value": 'dominance'},
                {"label": "Concreteness",
                 "value": 'concreteness'},
                {"label": "Date", "value": 'date'}],
            multi=False,
            value="valence",
            style={'width': "100%", "margin-top": "0.5rem"}
        ),
    ], style={"margin": "5px"}),
    html.Br(),
    html.Label([
        "Select Colour",
        dcc.Dropdown(
            id="select_color",
            options=[
                {"label": "Valence",
                 "value": 'valence'},
                {"label": "Arousal",
                 "value": 'arousal'},
                {"label": "Dominance",
                 "value": 'dominance'},
                {"label": "Concreteness",
                 "value": 'concreteness'},
                {"label": "Date",
                 "value": 'date'},
                {"label": "From", "value": 'from'},
                {"label": "To", "value": 'to'},
            ],
            multi=False,
            value="arousal",
            style={'width': "100%", "margin-top": "0.5rem"}
        ),
    ], style={"margin": "5px"}),
    html.Br(),
    dcc.Checklist(
        id="show_lett_content",
        options=[
            {'label': 'Show letter content on hover', 'value': 'content'},
        ],
        value=[]
    ),
    html.Br(),
    dcc.Checklist(
        id="use_average",
        options=[
            {'label': 'Use average', 'value': 'average'},
        ],
        value=[]
    ),
    html.Br(),
    html.H2("Artwork images", style={"margin": "0 5px"}),
    html.Br(),
    html.Label([
        "Select X axis",
        dcc.Dropdown(id="select_x_art",
                     options=[{"label": c, "value": c} for c in art_columns],
                     multi=False,
                     value='date',
                     style={'width': "100%", "margin-top": "0.5rem"}
                     ), ], style={"margin": "5px"}),
    html.Br(),
    html.Label([
        "Select Y axis",
        dcc.Dropdown(
            id="select_y_art",
            options=[{"label": c, "value": c} for c in art_columns],
            multi=False,
            value="valence",
            style={'width': "100%", "margin-top": "0.5rem"}
        ),
    ], style={"margin": "5px"}),
    html.Br(),
    html.Label([
        "Select Colour",
        dcc.Dropdown(
            id="select_color_art",
            options=[{"label": c, "value": c} for c in art_columns],
            multi=False,
            value="arousal",
            style={'width': "100%", "margin-top": "0.5rem"}
        ),
    ], style={"margin": "5px"}),
    html.Br(),
    dcc.Checklist(
        id="use_average_art",
        options=[
            {'label': 'Use average', 'value': 'average'},
        ],
        value=[]
    ),
    html.Br(),
    dcc.Graph(id="letter_scatter", figure={}),
    html.Br(),
    dcc.Graph(id="art_scatter", figure={})
], style={"margin": "0 auto", "max-width": "1150px"})


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components (LETTER)
@app.callback(
    [Output(component_id='letter_scatter', component_property="figure")],
    [Input(component_id='select_x', component_property='value'),
     Input(component_id='select_y', component_property='value'),
     Input(component_id='select_color', component_property='value'),
     Input(component_id='show_lett_content', component_property='value'),
     Input(component_id='use_average', component_property='value'),
     ]
)
def update_letter_scatter(x, y, color, show_lett_content, use_average):
    # dff = df.copy()
    lett_copy = lett.copy()
    tl = None
    if ("date" not in [x, y]):
        tl = "ols"
    if (len(use_average) > 0):
        lett_copy = lett.groupby(x, as_index=False)[
            [y, color]].agg([np.mean, np.std])
        lett_copy.columns = ['_'.join(x) for x in lett_copy.columns]
        lett_copy[x] = lett_copy.index
        print(lett_copy)
        y_temp = y
        y = y_temp+"_mean"
        color = color+"_mean"
        error_y = y_temp+"_std"
        # print(lett_copy)
    else:
        error_x = None
        error_y = None
    fig = px.scatter(lett_copy, x, y, color=color, trendline=tl,
                     title="Van Gogh's Letters", error_y=error_y)
    return [fig]


# Connect the Plotly graphs with Dash Components (ARTWORK)
@app.callback(
    [Output(component_id='art_scatter', component_property="figure")],
    [Input(component_id='select_x_art', component_property='value'),
     Input(component_id='select_y_art', component_property='value'),
     Input(component_id='select_color_art', component_property='value'),
     Input(component_id='use_average_art', component_property='value')]
)
def update_art_scatter(x, y, color, use_average):
    print(x, y, color)
    # container = "The year chosen by user was: {}".format(option_slctd)

    # dff = df.copy()
    art_copy = art.copy()

    # dff = dff[dff["Year"] == option_slctd]
    # dff = dff[dff["Affected by"] == "Varroa_mites"]
    tl = None
    if ("date" not in [x, y]):
        tl = "ols"
    if (len(use_average) > 0):
        art_copy = art.groupby(x).agg([np.mean, np.std])
        art_copy.columns = ['_'.join(x) for x in art_copy.columns]
        art_copy[x] = art_copy.index
        print(art_copy)
        y_temp = y
        y = y_temp+"_mean"
        color = color+"_mean"
        error_y = y_temp+"_std"
    else:
        error_y = None
    fig = px.scatter(art_copy, x, y, color=color,
                     trendline=tl, title="Van Gogh's Artworks", error_y=error_y)

    return [fig]


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
