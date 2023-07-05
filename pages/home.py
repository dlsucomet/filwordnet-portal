import dash
from dash import html, dcc
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
                dbc.NavLink('Senses and Sample Sentences', id='senses-link',
                            href='#', active='exact', className='sidebar-link'),
                dbc.NavLink('Network', href='#', active='exact', id='network-link',
                            className='sidebar-link'),
                dbc.NavLink('Plot (Filtered by Sense)', id='plot-sense-link',
                            href='#', active='exact', className='sidebar-link'),
                dbc.NavLink('Plot (Filtered by Source)', id='plot-source-link',
                            href='#', active='exact', className='sidebar-link'),
                dbc.NavLink('Embeddings', href='#', active='exact', id='embeddings-link',
                            className='sidebar-link'),
                dbc.NavLink('Export', href='#', active='exact', id='export-link',
                            className='sidebar-link'),
            ],
            vertical=True,
            pills=True
        ),
    ],
    style={'position': 'fixed',
           'paddingTop': '3em',             # Should be the same as padding-top of input_word
           'zIndex': '3000'}                # Should be higher than z-index of input_word
)


# =====================
# Input Field for Word
# =====================

input_word = dbc.Row([
    html.H5('Word to Search for'),
    html.Br(),
    dbc.InputGroup([
        html.Br(),
        dbc.Input(id='search-word'),
        dbc.Button('Search', color='dark',
                   id='search-word-submit-btn', n_clicks=0)
    ], style={'width': '60%'})
], style={'position': 'fixed',
          'width': 'inherit',
          'backgroundColor': 'white',
          'paddingTop': '3em',              # Should be the same as padding-top of sidebar
          'paddingBottom': '2.3em',
          'zIndex': '1000'},                # Should be lower than z-index of sidebar
    id='search-word-div'
)


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
        className='see-more',
        style={'fontSize': '0.9em',
               'color': 'gray', 'marginLeft': '1.5em'}
    )
], style={'fontSize': '1.10em'})

senses = dbc.Row([
    html.H2('Lorem', style={'marginTop': '5em'}, id='senses-word'),
    html.Div([
        dbc.Table(id='senses-container', children=[
            html.Tr([
                html.Td(
                    html.Span('Sense #1:'),
                    style={'width': '11%'}),
                html.Td(
                    html.Div([
                        html.Span(
                            'Definition lorem ipsum',
                            style={'fontSize': '0.9em'}
                        ),
                        html.Br(),
                        html.Span(
                            'Verb (v)',
                            style={'fontSize': '0.9em',
                                   'color': 'gray'}
                        ),
                        html.Br(),
                        html.Br(),
                        html.Span(
                            'Sample Sentences',
                            style={'fontSize': '0.9em'}
                        ),
                        html.Br(),
                        html.Ol([
                            html.Li(
                                html.Span('"Sentence lorem ipsum" (Source)')),
                            html.Li(
                                html.Span('"Sentence lorem ipsum" (Source)')),
                        ], style={'fontSize': '0.9em',
                                  'color': 'gray',
                                  'listStyleType': 'lower-alpha'
                                  }),
                        html.Span(['See more sample sentences ▼'],
                                  className='see-more',
                                  style={'fontSize': '0.9em',
                                         'color': 'gray'
                                         }),
                        html.Br(),
                        html.Br()
                    ]))], className='align-baseline'),
        ])

    ], style={'fontSize': '1.10em'})
])


# ========
# Network
# ========

network = dbc.Row([
    html.H4('Word Occurrence'),
    html.Br(),
    html.Br(),
    html.P('Choose a word occurrence community'),
    dcc.Dropdown(
        id='communities-dropdown',
        options=[
            {'label': 'Community 1', 'value': 1},
            {'label': 'Community 2', 'value': 2},
            {'label': 'Community 3', 'value': 3},
        ],
        value=1
    ),
    html.Br(),
    html.Br(),
    html.Br(),
    html.P(
        html.Div([
            dbc.Button([html.I(
                className='bi bi-arrow-clockwise me-2'),
                'Reset Display'],
                id='reset-network',
                color='light', size='sm', className='ms-3 table-button')
        ], style={'textAlign': 'right'})
    ),
    html.Div([
        cyto.Cytoscape(
            style={'width': '100%', 'height': '100vh'},
            id='network',
            layout={'name': 'circle'},
            stylesheet=[
                {
                    'selector': 'node',
                                'style': {
                                    'content': 'data(id)',
                                    'height': '5px',
                                    'width': '5px',
                                    'font-size': '10px'
                                }
                },
                {
                    'selector': 'edge',
                                'style': {
                                    'width': '0.5px',
                                }
                },
                {
                    'selector': '.shaded',
                                'style': {
                                    'background-color': '#254b5d',
                                    'line-color': '#254b5d',
                                    'height': '20px',
                                    'width': '20px'
                                }
                }
            ]
        )
    ])
], style={'width': '96%'})


# =========================
# Plot (Filtered by Sense)
# =========================

plot_by_sense = dbc.Row([
    html.H4('Usage Over Time Per Sense (Filtered by Sense)'),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div([
            'Show me how the usage of ',
            # html.Div(
            html.Div([
                dcc.Dropdown(
                    id='sense-dropdown',
                    style={
                        # 'padding-left': '1%',
                        # 'padding-right': '1%',
                        # 'width': '40%',
                        'verticalAlign': 'middle'}
                ),
            ], style={'width': '20%', 'marginLeft': '1%', 'marginRight': '1%'},
            ),

            # ),
            ' evolves over time',

        ],  className='d-flex flex-row align-middle', style={'alignItems': 'center'}
            # style={'display': 'inline-block'}
            # className='d-inline'
        ),

        html.Br(),

        # dbc.Checklist(
        #    id="checklist-sense",
        #    inline=True
        # ),
        dcc.Graph(id="graph-sense")
    ])
])


# ==========================
# Plot (Filtered by Source)
# ==========================

plot_by_source = dbc.Row([
    html.H4('Usage Over Time Per Sense (Filtered by Source)'),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div([
            'Show me how the usage of sense in ',
            html.Div([
                dcc.Dropdown(
                    id='source-dropdown',
                    style={
                        'verticalAlign': 'middle'}
                ),
            ], style={'width': '20%', 'marginLeft': '1%', 'marginRight': '1%'},
            ),
            ' evolves over time'
        ],  className='d-flex flex-row align-middle', style={'alignItems': 'center'}
        ),
        # dbc.Checklist(
        #    id="checklist-source",
        #    inline=True
        # ),
        dcc.Graph(id="graph-source")
    ])
])


# ===========
# Embeddings
# ===========

embeddings = dbc.Row([
    html.H4('Sense Embeddings'),
    html.Br(),
    html.Br(),
    html.Div([
        dbc.Checklist(
            id="embeddings-checklist",
            # options=["Source 1", "Source 2", "Source 3"],
            # value=["Source 1"],
            inline=True,
            style={'display': 'none'}
        ),
        dcc.Graph(id="embeddings")  # ,
        # figure=px.scatter_3d(px.data.iris(),
        #                     x='sepal_length', y='sepal_width', z='petal_width',
        #                     color='species', hover_data=['petal_width'])),
    ])
])


# =======
# Export
# =======

export = dbc.Row([
    html.H4('Export Data'),
    html.Br(),
    html.Br(),
    html.Ul([
        html.Li('Senses and Sample Sentences (JSON)'),
        html.Li('Embeddings (CSV)'),
    ], style={'marginLeft': '2em'}),
])


# =====
# Body
# =====

body = dbc.Row([
    dbc.Col(
        dbc.Container([
            input_word,
            senses,
            html.Br(id='network-row'),
            network,
            html.Br(id='plot-sense-row'),
            plot_by_sense,
            html.Br(id='plot-source-row'),
            html.Br(),
            plot_by_source,
            html.Br(id='embeddings-row'),
            html.Br(),
            embeddings,
            html.Br(id='export-row'),
            export
        ])
    ),

    dbc.Col(sidebar, width=3)
])

# ============
# Main Layout
# ============

layout = dbc.Container([
    html.Br(),
    html.Br(),
    body,
    html.Br()           # Should be here, not in app.py
                        # Otherwise, a portion of the footer can be seen when body
                        #    has not completely loaded
],
    fluid=True,
    style={'paddingLeft': '6em', 'paddingRight': '6em'}
)
