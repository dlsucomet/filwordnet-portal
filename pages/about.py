import dash
from dash import html


dash.register_page(__name__, path='/about', name='About')

layout = html.Div()
