import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

import dash_cytoscape as cyto


dash.register_page(__name__, path='/', name='FilWordNet | Discover')


# ==========================
# Local Navigation Side-Bar
# ==========================

sidebar = html.Div(
    id='home-sidebar',
    children=[
        html.H5('Contents'),
        html.Hr(),
        dbc.Nav([
            dbc.NavLink('Word Senses and Sample Sentences', id='senses-link',
                        href='#', active='exact', className='sidebar-link'),
            dbc.NavLink('Word Co-Occurrence', active='exact', id='network-link',
                        className='sidebar-link'),
            dbc.NavLink('Usage of Word Senses Over Time', id='plot-sense-link',
                        active='exact', className='sidebar-link'),
            dbc.NavLink('Usage of Word Across Sources Over Time', id='plot-source-link',
                        active='exact', className='sidebar-link'),
            dbc.NavLink('Word Sense Embeddings', active='exact', id='embeddings-link',
                        className='sidebar-link'),
            dbc.NavLink('Export Data', active='exact', id='export-link',
                        className='sidebar-link'),
        ], vertical=True, pills=True),
    ], 
    style={'position': 'fixed',
            'paddingTop': '3em',             # Should be the same as padding-top of input_word
            'zIndex': '3000'},                # Should be higher than z-index of input_word
    hidden=True
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
    dcc.Loading(
        [html.H2('Lorem', style={'marginTop': '5em'}, id='senses-word'),
         html.Div([
             dbc.Table(
                 id='senses-container',
                 children=[
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
                            ])
                        )
                    ], className='align-baseline'),
                 ]
             )
         ], style={'fontSize': '1.10em'})]
    )
])


# ========
# Network
# ========

network = dbc.Row([
    html.H4('Word Co-Occurrence'),
    html.Br(),
    html.Br(),
    html.P('Select a word co-occurrence community'),
    dcc.Dropdown(
        id='communities-dropdown',
        value=0
    ),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Label('Select the size of the displayed community'),
    html.Br(),
    html.Br(),
    dcc.Slider(1, 4,
               marks={1: '1 (Closest Co-Occurring Words)',
                      2: '2',
                      3: '3',
                      4: '4 (All Co-Occurring Words)'},
               value=1,
               id='communities-ego-network-dist'),
    html.Br(),
    html.Br(),
    html.Br(),
    dbc.Label('Select the display layout'),

    dbc.RadioItems(
        id='communities-layout',
        options=[
            {'value': 'circle', 'label': 'Circle',
             'label_id': 'circle'},
            {'value': 'grid', 'label': 'Grid',
             'label_id': 'grid'}
        ],
        value='circle',
        inline=True,
        className='ms-3'
    ),
    html.Br(),
    html.P(
        html.Div([
            dbc.Button([html.I(
                className='bi bi-arrow-clockwise me-2'),
                'Reset Display'],
                id='reset-network',
                color='light', size='sm', className='ms-3 table-button',
                style={'border': '1px solid rgb(211, 211, 211)', 'backgroundColor': 'white'})
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
                                    'background-color': 'black',
                                    'line-color': 'black',
                                    'height': '10px',
                                    'width': '10px'
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
    html.H4('Usage of Word Senses Over Time'),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div([
            'Show me how the usage of ',
            html.Div([
                dcc.Dropdown(
                    id='sense-dropdown',
                    style={
                        'verticalAlign': 'middle'}
                ),
            ], style={'width': '20%', 'marginLeft': '1%', 'marginRight': '1%'},
            ),

            ' of', html.Span(
                id='word-plot-sense', style={'white-space': 'pre'}, className='fw-bold'), 'evolves over time',

        ],  className='d-flex flex-row align-middle', style={'alignItems': 'center'}
        ),
        html.Div(id='sense-sample-sentence'),

        html.Br(),

        dcc.Loading(dcc.Graph(id="graph-sense"))
    ])
])


# ==========================
# Plot (Filtered by Source)
# ==========================

plot_by_source = dbc.Row([
    html.H4('Usage of Word Across Sources Over Time'),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div([
            'Show me how the usage of ', html.Span(
                id='word-plot-source', style={'white-space': 'pre'}, className='fw-bold'), 'in',
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

        dcc.Loading(dcc.Graph(id="graph-source"))
    ])
])


# ===========
# Embeddings
# ===========

embeddings = dbc.Row([
    html.H4('Word Sense Embeddings'),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div(
            'Three-dimensional projection of word sense embeddings obtained via principal component analysis (PCA)'),
        dcc.Loading(dcc.Graph(id="embeddings"))
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
        html.Li('Word Senses and Sample Sentences (JSON)'),
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

            html.Div(
                id='home-body-container',
                children = [
                    senses,
                    # html.Br(id='network-row'),
                    # network,
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
                ],
                hidden=True
            ),
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
