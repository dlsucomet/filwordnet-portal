
import dash
import dash_bootstrap_components as dbc

from flask import Flask
from dash import html

import callbacks.home.callbacks
import callbacks.home.scroll_callbacks

server = Flask(__name__, static_folder='static')
app = dash.Dash(__name__, use_pages=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP,
                                      dbc.icons.BOOTSTRAP, dbc.icons.FONT_AWESOME],
                server=server)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink('Discover', href='/', active='exact')),
        dbc.NavItem(dbc.NavLink(
                    'About', href='/about', active='exact')),
        dbc.NavItem(dbc.NavLink(
                    'People', href='/people', active='exact')),
        dbc.NavItem(dbc.NavLink('Publications',
                                href='/publications', active='exact')),
    ],
    brand=[html.Img(src="static/assets/filwordnet-logo.png",
                    height="30px", style={'marginRight': '30px'}), 'FilWordNet'],
    brand_href='/',
    color='dark',
    dark=True,
    style={'position': 'fixed', 'zIndex': '100000'}
)

app.layout = dbc.Container([
    dbc.Row([
        navbar,
        dash.page_container
    ]),

    dbc.Row(dbc.Col('Copyright Lorem Ipsum', class_name='text-center'),
            class_name='bg-dark text-white p-3')
], fluid=True)


callbacks.home.callbacks.init_callback(app)
callbacks.home.scroll_callbacks.init_callback(app)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port='8050', debug=True)
