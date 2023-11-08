import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dash_table, html

dash.register_page(__name__, path='/about', name='About')

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
        ], style={'paddingTop': '2em',
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
            ], className='px-0'),
            style={'paddingRight': '5em',
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

            ], className='mt-3 px-0'),
            style={'paddingRight': '8em',
                   'paddingBottom': '1.75em'}
        )
    ])


layout = dbc.Container([
    html.Br(),
    html.Br(),
    html.Br(),
    body_about,
    html.Br()
])
