import dash
from dash import html


dash.register_page(__name__, path='/people', name='People')

layout = html.Div()
