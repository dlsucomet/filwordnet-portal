
import dash
import dash_bootstrap_components as dbc

from dash import html, dcc

import callbacks.home.sense.callbacks
import callbacks.home.network.callbacks
import callbacks.home.plot.callbacks
import callbacks.home.embeddings.callbacks

import callbacks.home.scroll_callbacks
import callbacks.home.home_callbacks

from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.environ.get("API_URL")

app = dash.Dash(__name__, use_pages=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP,
                                      dbc.icons.BOOTSTRAP, dbc.icons.FONT_AWESOME])
server = app.server

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

    # dbc.Row(dbc.Col('Copyright © 2023. Center for Complexity and Emerging Technologies, De La Salle University', class_name='text-center'),
    #        class_name='bg-dark text-white p-3'),

    dcc.Store(
        id='submitted-word',
        storage_type='session'
    )

], fluid=True)


callbacks.home.sense.callbacks.init_callback(app, API_URL)
callbacks.home.network.callbacks.init_callback(app, API_URL)
callbacks.home.plot.callbacks.init_callback(app, API_URL)
callbacks.home.embeddings.callbacks.init_callback(app, API_URL)

callbacks.home.scroll_callbacks.init_callback(app)
callbacks.home.home_callbacks.init_callback(app)

if __name__ == '__main__':
    app.run_server(port='8049', debug=True)
