
import dash
import dash_bootstrap_components as dbc

from flask import Flask
from dash import html

server = Flask(__name__, static_folder='static')
app = dash.Dash(__name__, use_pages=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP,
                                      dbc.icons.BOOTSTRAP, dbc.icons.FONT_AWESOME],
                server=server)

app.layout = dbc.Container([
    dbc.Row([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink('Home', href='/', active='exact')),
                dbc.NavItem(dbc.NavLink(
                    'About', href='/about', active='exact')),
                dbc.NavItem(dbc.NavLink(
                    'People', href='/people', active='exact')),
                dbc.NavItem(dbc.NavLink('Publications',
                            href='/publications', active='exact')),
            ],
            brand=[html.Img(src="static/assets/filwordnet-logo.png",
                            height="30px", style={'margin-right': '30px'}), 'FilWordNet'],
            brand_href='/',
            color='dark',
            dark=True,
            style={'position': 'fixed', 'z-index': '100000'}
        ),

        dash.page_container
    ])
], fluid=True)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port='8050', debug=True)
