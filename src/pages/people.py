import dash
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(__name__, path='/people', name='People')

layout = dbc.Container([
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div("Hello World")
])
