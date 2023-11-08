import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dash_table, dcc, html

dash.register_page(__name__, path='/', name='FilWordNet | Discover')


# ==========================
# Local Navigation Side-Bar
# ==========================

df_data = pd.DataFrame([['Books', '173'],
                        ['Wikipedia', '129,302'],
                        ['Dictionary', '56,608'],
                        ['News Sites', '445,685'],
                        ['Reddit', '2,053,405'],
                        ['Twitter', '54,457,383'],
                        ['PinoyExchange', '347,319'],
                        ['Wattpad', '22'],
                        ['LyricsFreak', '727'],
                        ['YouTube', '44,823,774']])

df_data = df_data.rename(columns={0: 'Source', 1: 'Data Count'})

df_tokens = pd.DataFrame([['Books', '8,907,568', '23'],
                          ['Wikipedia', '9,177,188', '32'],
                          ['News Sites', '94,466,149', '20'],
                          ['Reddit', '30,041,725', '15'],
                          ['Twitter', '214,649,994', '11'],
                          ['PinoyExchange', '64,289,785', '15'],
                          ['Wattpad', '15,433', '23'],
                          ['LyricsFreak', '87,723', '13'],
                          ['YouTube', '578,128,702', '13']])

df_tokens = df_tokens.rename(
    columns={0: 'Source', 1: 'Total Num. of Tokens', 2: 'Mean Sentence Length'})

sidebar = html.Div(
    id='home-sidebar',
    children=[
        html.H5('Contents'),
        html.Hr(),
        dbc.Nav([
            dbc.NavLink('Word Senses & Sample Sentences', id='senses-link',
                        href='#', active='exact', className='sidebar-link', style={'white-space': 'nowrap'}),
            dbc.NavLink('Usage of Word Senses Over Time', id='plot-sense-link',
                        active='exact', className='sidebar-link', style={'white-space': 'nowrap'}),
            dbc.NavLink('Usage Across Sources Over Time', id='plot-source-link',
                        active='exact', className='sidebar-link', style={'white-space': 'nowrap'}),
            dbc.NavLink('Word Sense Embeddings', active='exact', id='embeddings-link',
                        className='sidebar-link', style={'white-space': 'nowrap'}),
            dbc.NavLink('Co-Occurring Words', active='exact', id='network-link',
                        className='sidebar-link', style={'white-space': 'nowrap'}),
            dbc.NavLink('Export Data', active='exact', id='export-link',
                        className='sidebar-link', style={'white-space': 'nowrap'}),
        ], vertical=True, pills=True),
    ],
    style={'position': 'fixed',
           'paddingRight': '4em',
           'paddingTop': '3em',             # Should be the same as padding-top of input_word
           'zIndex': '3000'},               # Should be higher than z-index of input_word
    hidden=True
)


# =====================
# Input Field for Word
# =====================

input_word = dbc.Row([
    html.H5('Enter a word'),
    html.Br(),
    dbc.InputGroup([
        html.Br(),
        dbc.Input(id='search-word', n_submit=0),
        dbc.Button('Search', color='dark',
                   id='search-word-submit-btn', n_clicks=0)
    ], style={'width': '62%'})
], style={'position': 'fixed',
          'width': 'inherit',
          'backgroundColor': 'white',
          'paddingTop': '3em',              # Should be the same as padding-top of sidebar
          'paddingBottom': '2.3em',
          'zIndex': '1050'},                # Should be lower than z-index of sidebar,
                                            # Exact value (obtained via trial and error). Do not change!
    id='search-word-div'
)


# ==========================
# Senses & Sample Sentences
# ==========================

senses = dbc.Row([
    html.Div(
        dcc.Loading(
            html.H2('', id='senses-word')
        ), style={'marginTop': '10em'}
    ),
    html.Div([
        dbc.Table(id='senses-container')
    ], style={'fontSize': '1.10em'})
])


# ========
# Network
# ========

network = dbc.Row([
    html.H2('Co-Occurring Words'),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div([
            'Words that frequently appear together with ',
             html.Span(
                 children=[
                     html.Span(' ', id='input-word-network'),
                     html.Span(' '),
                     html.I(
                         className='bi bi-info-circle',
                     ),
                 ],
                 id='word-plot-network', n_clicks=0, style={'white-space': 'pre'}, className='fw-bold')
             ], className='mb-2 mt-2'),

        dcc.Dropdown(
            id='communities-dropdown',
            className='mb-4',
            clearable=False,
            value=0
        ),

        dcc.Loading([
            html.Div(id='network-sample-sentence'),
            html.Br(),
            html.Div(id='network-cooccurring-words')
        ])
    ], className='pe-5')
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
    style={'zIndex': '500000'}
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
    html.Div([
        html.Div([
            'Show me how the usage of ',
            html.Div([
                dcc.Dropdown(
                    id='sense-dropdown',
                    clearable=False,
                    style={
                        'verticalAlign': 'middle'}
                ),
            ], style={'width': '20%', 'marginLeft': '1%', 'marginRight': '1%'},
            ),

            ' of', html.Span(
                children=[
                    f' ',
                    html.I(
                        className='bi bi-info-circle',
                    ),
                    f' '
                ],
                id='word-plot-sense', n_clicks=0, style={'white-space': 'pre'}, className='fw-bold'), 'evolves over time',

        ],  className='d-flex flex-row align-middle', style={'alignItems': 'center'}
        ),
        dcc.Loading(
            [html.Div(id='sense-sample-sentence'),
             word_plot_modal,
             html.Br(),
             dcc.Graph(id="graph-sense")]
        )
    ])
])


# ==========================
# Plot (Filtered by Source)
# ==========================

plot_by_source = dbc.Row([
    html.H4('Usage Across Sources Over Time'),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div([
            'Show me how the usage of ',
            html.Span(
                children=[
                    f' ',
                    html.I(
                        className='bi bi-info-circle',
                    ),
                    f' '
                ],
                id='word-plot-source', n_clicks=0, style={'white-space': 'pre'}, className='fw-bold'), 'in',
            html.Div([
                dcc.Dropdown(
                    id='source-dropdown',
                    clearable=False,
                    style={
                        'verticalAlign': 'middle'}
                ),
            ], style={'width': '20%', 'marginLeft': '1%', 'marginRight': '1%'},
            ),
            ' evolves over time'
        ],  className='d-flex flex-row align-middle', style={'alignItems': 'center'}),

        word_plot_modal,

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
        html.Div(
            'Data processing is ongoing for senses marked with an asterisk (*)',
            className='small mt-3', style={'color': 'gray'}
        ),
        dcc.Loading(dcc.Graph(id="embeddings"))
    ])
])


# =======
# Export
# =======

export = dbc.Row([
    html.H4('Export Data', className='mt-3'),
    html.Br(),
    html.Br(),
    html.Ul([
        html.Li(html.Span('Word Senses, Sample Sentences, Usage & Co-Occurring Words (JSON)',
                className='link-primary', n_clicks=0,
                id='export-senses')),
        html.Li(html.Span('Word Sense Embeddings (CSV)',
                className='link-primary', n_clicks=0,
                id='export-embeddings')),
    ], style={'marginLeft': '2em'}, className='mt-2'),

    dcc.Download(
        id='download-embeddings'
    ),

    dcc.Download(
        id='download-senses'
    )
])


# =====
# Body
# =====

body = dbc.Row([
    dbc.Col(
        dbc.Container([
            input_word,

            html.Div(id='search-word-error-container', children=[
                html.Div(id='search-word-error')
            ], style={'paddingTop': '10em'}, hidden=True),

            html.Div(
                id='home-body-container',
                children=[
                    html.Br(id='senses-row', style={'display': 'none'}),
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

        ]),
        width=9,
        style={'paddingLeft': '5em',
               'paddingRight': '3em'}
    ),

    dbc.Col(sidebar, width=3)
])

body_about = html.Div(
    id='body-about',
    children=[
        dbc.Row([
            dbc.Col([
                html.H4(
                    'FilWordNet: Building a Rich Lexicon for Low-Resource Philippine Languages'),
                html.P('Filipino WordNet or FilWordNet is a language resource for Filipino and Philippine English as used in the online realm. The project aims to capture word meanings and their contexts — and how their usages evolve over time — through analyzing textual data via network science and natural language processing techniques.',
                       className='mt-3'),
                html.P('By creating a rich digital lexicon, FilWordNet crucially fills a void in local language resources and could pave the way for enhancing several downstream applications such as sentiment analysis and translation.')
            ], width=9, className='px-0'),

            dbc.Col([
                html.Div(
                    html.Img(src='assets/images/filwordnet-body.png',
                             style={'width': '45%',
                                    'height': 'auto'}),
                    className='text-center',
                    style={'paddingTop': '1em'}
                )
            ],  width=3)
        ], style={'paddingTop': '10em',
                  'paddingLeft': '5.7em',
                  'paddingBottom': '1.75em'}),

        dbc.Row(
            dbc.Col([
                html.H4('News'),

                html.Ul([
                    html.Li([
                        html.P([html.B('November 2023: '),
                            html.Span(className='ms-2'),
                            'We added 59,784 more data, collected from multiple news sites and Reddit, to our database.']),
                    ]),
                    html.Li([
                        html.P([html.B('September 2023: '),
                            html.Span(className='ms-2'),
                            'Our paper "Towards the Creation of the Filipino Wordnet: A Two-Way Approach" was accepted for paper presentation at the ',
                                html.B(
                                'International Conference on Asian Language Processing 2023 (IALP 2023)'),
                                ', organized by the Chinese and Oriental Languages Information Processing Society. Research assistants Dan John Velasco and Mark Edward Gonzales will be heading to Singapore on November 18 to present our work.']),
                    ]),
                ], className='mt-3')
            ]),
            style={'paddingLeft': '5em',
                   'paddingRight': '5em',
                   'paddingBottom': '1.75em'}
        ),

        dbc.Row(
            dbc.Col([
                html.H4('Statistics'),

                html.P([
                    'We have a total of ',
                    html.B('101,967,079 data'),
                    ' collected from the following sources:'
                ],
                    className='mt-3'),
                dash_table.DataTable(
                    df_data.to_dict('records'),
                    style_table={'width': '25%', 'paddingLeft': '1em'},
                    style_cell={
                        'fontFamily': 'var(--bs-font-sans-serif)', 'padding': '5px'},
                ),

                html.P([
                    'Our corpus has ',
                    html.B('935,371,326 tokens'),
                    ', of which ',
                    html.B('5,370,667 are unique'),
                    ':'
                ],
                    className='mt-4'),
                dash_table.DataTable(
                    df_tokens.to_dict('records'),
                    style_table={'width': '50%', 'paddingLeft': '1em'},
                    style_cell={
                        'fontFamily': 'var(--bs-font-sans-serif)', 'padding': '5px'},
                ),

            ], className='mt-3'),
            style={'paddingLeft': '5em',
                   'paddingRight': '8em',
                   'paddingBottom': '1.75em'}
        )
    ])

# ============
# Main Layout
# ============

layout = dbc.Container([
    html.Br(),
    html.Br(),
    body,
    body_about,
    html.Br()           # Should be here, not in app.py
                        # Otherwise, a portion of the footer can be seen when body
                        #    has not completely loaded
], fluid=True)
