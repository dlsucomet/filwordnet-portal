import dash
from dash import html
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/', name='Home')

sidebar = html.Div(
    [
        html.H5('Contents'),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink('Senses and Sample Sentences',
                            href='/', active='exact'),
                dbc.NavLink('Network', href='#', active='exact'),
                dbc.NavLink('Plot (Filtered by Sense)',
                            href='#', active='exact'),
                dbc.NavLink('Plot (Filtered by Source)',
                            href='#', active='exact'),
                dbc.NavLink('Embeddings', href='#', active='exact'),
                dbc.NavLink('Export', href='#', active='exact'),
            ],
            vertical=True,
            pills=True
        ),
    ],
    style={'position': 'fixed'},
)

layout = dbc.Container([
    html.Br(),
    dbc.Row([
        html.H5('Word to Search for'),
        html.Br(),
        dbc.InputGroup([
            html.Br(),
            dbc.Input(),
            dbc.Button('Search')
        ])
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(),
        dbc.Col(sidebar, width=3),
    ])
], fluid=True)
