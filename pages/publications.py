import dash
from dash import html


dash.register_page(__name__, path='/publications', name='Publications')

layout = html.Div()
