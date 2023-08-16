
import dash
import dash_bootstrap_components as dbc

from flask import Flask
from dash import html, dcc

import callbacks.home.sense_callbacks
import callbacks.home.network_callbacks
import callbacks.home.plot_callbacks
import callbacks.home.embeddings_callbacks

import callbacks.home.scroll_callbacks

from dotenv import load_dotenv
import os

load_dotenv()

print(os.environ.get("API_URL"))

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
    style={'position': 'fixed', 'zIndex': '100000',
           'padding-left': '6em', 'padding-right': '6em'},
    fluid=True
)

app.layout = dbc.Container([
    dbc.Row([
        navbar,
        dash.page_container
    ]),

    dbc.Row(dbc.Col('Copyright © 2023. Center for Complexity and Emerging Technologies, De La Salle University', class_name='text-center'),
            class_name='bg-dark text-white p-3'),

    dcc.Store(
        id='submitted-word',
        storage_type='session'
    )

], fluid=True)


callbacks.home.sense_callbacks.init_callback(app)
callbacks.home.network_callbacks.init_callback(app)
callbacks.home.plot_callbacks.init_callback(app)
callbacks.home.embeddings_callbacks.init_callback(app)

callbacks.home.scroll_callbacks.init_callback(app)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port='8050', debug=True)
