import dash
from dash import html
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/', name='Home')


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


input_word = dbc.Row([
    html.H5('Word to Search for'),
    html.Br(),
    dbc.InputGroup([
        html.Br(),
        dbc.Input(),
        dbc.Button('Search', color='dark')
    ])
], style={'position': 'fixed', 'width': '50%', 'backgroundColor': 'white', 'paddingTop': '3em'})


# =======
# Senses
# =======

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
    html.H2('Lorem'),
    html.Ol([
        simple_sense,
        html.Br(),
        sense_with_see_more

    ], style={'marginTop': '6.5em', 'marginLeft': '2em'})
])

layout = dbc.Container([
    html.Br(),

    html.Br(),

    dbc.Row([
        dbc.Col(
            dbc.Container(
                [input_word, senses]
            )
        ),

        dbc.Col(sidebar, width=3),
    ])
],
    fluid=True,
    style={'paddingLeft': '6em', 'paddingRight': '6em'}
)
