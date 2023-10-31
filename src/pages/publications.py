import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/publications', name='Publications')

layout = dbc.Container([
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div("Hello World")
])
