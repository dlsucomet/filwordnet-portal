import dash
from dash import html
import dash_bootstrap_components as dbc

import dash_cytoscape as cyto


dash.register_page(__name__, path='/', name='Home')


# ==========================
# Local Navigation Side-Bar
# ==========================

sidebar = html.Div(
    [
        html.H5('Contents'),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink('Senses and Sample Sentences',
                            href='/', active='exact'),
                dbc.NavLink('Network', href='#', active='exact'),
                dbc.NavLink('Plot (Filtered by Sense)',
                            href='#', active='exact'),
                dbc.NavLink('Plot (Filtered by Source)',
                            href='#', active='exact'),
                dbc.NavLink('Embeddings', href='#', active='exact'),
                dbc.NavLink('Export', href='#', active='exact'),
            ],
            vertical=True,
            pills=True
        ),
    ],
    style={'position': 'fixed', 'paddingTop': '3em'},
)


# =====================
# Input Field for Word
# =====================

input_word = dbc.Row([
    html.H5('Word to Search for'),
    html.Br(),
    dbc.InputGroup([
        html.Br(),
        dbc.Input(),
        dbc.Button('Search', color='dark')
    ])
], style={'position': 'fixed', 'width': '50%', 'backgroundColor': 'white', 'paddingTop': '3em', 'paddingBottom': '2.3em'})


# ==========================
# Senses & Sample Sentences
# ==========================

simple_sense = html.Li([
    html.Span(
        'Noun',
        style={'fontStyle': 'italic'}
    ),
    html.Br(),
    html.Span(
        'Definition lorem ipsum',
        style={'fontSize': '0.9em', 'marginLeft': '1.5em'}
    ),
    html.Br(),
    html.Span(
        '"Sentence lorem ipsum" (Source)',
        style={'fontSize': '0.9em',
               'color': 'gray', 'marginLeft': '1.5em'}
    )
], style={'fontSize': '1.10em'})

sense_with_see_more = html.Li([
    html.Span(
        'Verb',
        style={'fontStyle': 'italic'}
    ),
    html.Br(),
    html.Span(
        'Definition lorem ipsum',
        style={'fontSize': '0.9em', 'marginLeft': '1.5em'}
    ),
    html.Br(),
    html.Span(
        '"Sentence lorem ipsum" (Source)',
        style={'fontSize': '0.9em',
               'color': 'gray', 'marginLeft': '1.5em'}
    ),
    html.Br(),
    html.Span(
        'See more sample sentences ▼',
        style={'fontSize': '0.9em',
               'color': 'gray', 'marginLeft': '1.5em'}
    )
], style={'fontSize': '1.10em'})

senses = dbc.Row([
    html.H2('Lorem', style={'marginTop': '5em'}),
    html.Ol([
        simple_sense,
        html.Br(),
        sense_with_see_more
    ], style={'marginTop': '1.5em', 'marginLeft': '2em'})
])


# ========
# Network
# ========

nodes = [
    {
        'data': {'id': short, 'label': label},
        'position': {'x': 20 * lat, 'y': -20 * long}
    }
    for short, label, long, lat in (
        ('la', 'Lorem', 34.03, -118.25),
        ('nyc', 'Ipsum 2', 40.71, -74),
        ('to', 'Ipsum 3', 43.65, -79.38),
        ('mtl', 'Ipsum 4', 45.50, -73.57),
        ('van', 'Ipsum 5', 49.28, -123.12),
        ('chi', 'Ipsum 6', 41.88, -87.63),
        ('bos', 'Ipsum 7', 42.36, -71.06),
        ('hou', 'Ipsum 8', 29.76, -95.37)
    )
]

edges = [
    {'data': {'source': source, 'target': target}}
    for source, target in (
        ('van', 'la'),
        ('la', 'chi'),
        ('hou', 'chi'),
        ('to', 'mtl'),
        ('mtl', 'bos'),
        ('nyc', 'bos'),
        ('to', 'hou'),
        ('to', 'nyc'),
        ('la', 'nyc'),
        ('nyc', 'bos')
    )
]

elements = nodes + edges

network = dbc.Row([
    html.H4('Network'),
    html.Div([
        cyto.Cytoscape(
            layout={'name': 'breadthfirst', 'roots': '[id = "la"]'},
            style={'width': '100%', 'height': '20em'},
            elements=elements
        )
    ])
])


# =====
# Body
# =====

body = dbc.Row([
    dbc.Col(
        dbc.Container(
            [input_word,
             senses,
             html.Br(),
             network]
        )
    ),

    dbc.Col(sidebar, width=3),
])

# ============
# Main Layout
# ============

layout = dbc.Container([
    html.Br(),
    html.Br(),
    body,
],
    fluid=True,
    style={'paddingLeft': '6em', 'paddingRight': '6em'}
)
