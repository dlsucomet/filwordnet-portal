import dash
from dash import html, dcc
import dash_bootstrap_components as dbc


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
            dbc.NavLink('Usage of Word Senses Over Time', id='plot-sense-link',
                        active='exact', className='sidebar-link'),
            dbc.NavLink('Usage of Word Across Sources Over Time', id='plot-source-link',
                        active='exact', className='sidebar-link'),
            dbc.NavLink('Word Sense Embeddings', active='exact', id='embeddings-link',
                        className='sidebar-link'),
            dbc.NavLink('Co-Occurring Words', active='exact', id='network-link',
                        className='sidebar-link'),
            dbc.NavLink('Export Data', active='exact', id='export-link',
                        className='sidebar-link'),
        ], vertical=True, pills=True),
    ],
    style={'position': 'fixed',
           'paddingTop': '3em',             # Should be the same as padding-top of input_word
           'zIndex': '3000'},               # Should be higher than z-index of input_word
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

senses = dbc.Row([
    dcc.Loading(html.Div(
        html.H2('', style={'marginTop': '5em'}, id='senses-word')
    )),
    dcc.Loading(html.Div([
        dbc.Table(id='senses-container')
    ], style={'fontSize': '1.10em'}))
])


# ========
# Network
# ========

network = dbc.Row([
    html.H2('Co-Occurring Words', style={'marginTop': '5em'}),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div([
            'Words that frequently appear together with ',
            html.Span(id='input-word-network')
        ], className='mb-2 mt-2'),

        dcc.Dropdown(
            id='communities-dropdown',
            value='Sense 1'
        ),

        html.Br(),

        dcc.Loading(html.Div(id='network-cooccurring-words'))
    ])
])

# =========================
# Plot (Modal)
# =========================

word_plot_modal = dbc.Modal(
    id='word-plot-modal',
    is_open=False,
    size='lg',
    scrollable=True,
    centered=False,
    # Should be higher than z-index of sidebar
    style={'zIndex': '5000'}
)

# =========================
# Plot (Word)
# =========================

word_plot = html.Span(
    children=[
        f' word ',
        html.I(
            className='bi bi-info-circle',
        ),
        f' '
    ],
    id='word-plot', n_clicks=0, style={'white-space': 'pre'}, className='fw-bold')

# =========================
# Plot (Filtered by Sense)
# =========================

plot_by_sense = dbc.Row([
    html.H4('Usage of Word Senses Over Time'),
    html.Br(),
    html.Br(),
    dcc.Loading(
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
                    children=[
                        f' word ',
                        html.I(
                            className='bi bi-info-circle',
                        ),
                        f' '
                    ],
                    id='word-plot-sense', n_clicks=0, style={'white-space': 'pre'}, className='fw-bold'), 'evolves over time',

            ],  className='d-flex flex-row align-middle', style={'alignItems': 'center'}
            ),
            html.Div(id='sense-sample-sentence'),

            word_plot_modal,

            html.Br(),

            dcc.Graph(id="graph-sense")
        ])
    )
])


# ==========================
# Plot (Filtered by Source)
# ==========================

plot_by_source = dbc.Row([
    html.H4('Usage of Word Across Sources Over Time'),
    html.Br(),
    html.Br(),
    dcc.Loading(
        html.Div([
            html.Div([
                'Show me how the usage of ',
                html.Span(
                    children=[
                        f' word ',
                        html.I(
                            className='bi bi-info-circle',
                        ),
                        f' '
                    ],
                    id='word-plot-source', n_clicks=0, style={'white-space': 'pre'}, className='fw-bold'), 'in',
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

            word_plot_modal,

            dcc.Graph(id="graph-source")
        ])
    )
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
                children=[
                    senses,
                    html.Br(id='plot-sense-row'),
                    plot_by_sense,
                    html.Br(id='plot-source-row'),
                    html.Br(),
                    plot_by_source,
                    html.Br(id='embeddings-row'),
                    html.Br(),
                    embeddings,
                    html.Br(id='network-row'),
                    network,
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
])
