import dash
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(__name__, path='/publications', name='Publications')

layout = dbc.Container([
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div("Hello World")
])
