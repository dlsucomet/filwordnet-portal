import dash
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(__name__, path='/people', name='People')

people = html.Div(
    children=[
        dbc.Row([
            dbc.Col([
                html.H4('Proponents', className='pb-1'),
                html.Ul([
                    html.Li([
                        'Dr. Briane Paul V. Samson (Project Leader)',
                        html.Br(),
                        html.Span('Center for Complexity and Emerging Technologies',
                                  style={'color': 'gray'}),
                        html.Br(),
                        html.Span('Advanced Research Institute for Informatics, Networking and Computing',
                                  style={'color': 'gray'}),
                        html.Br(),
                        html.Span('De La Salle University',
                                  style={'color': 'gray'}),
                    ], className='pb-3'),

                    html.Li([
                        'Dr. Charibeth K. Cheng',
                        html.Br(),
                        html.Span('Center for Language Technologies',
                                  style={'color': 'gray'}),
                        html.Br(),
                        html.Span('Advanced Research Institute for Informatics, Networking and Computing',
                                  style={'color': 'gray'}),
                        html.Br(),
                        html.Span('De La Salle University',
                                  style={'color': 'gray'}),
                    ], className='pb-3'),

                    html.Li([
                        'Ms. Unisse C. Chua',
                        html.Br(),
                        html.Span('Center for Complexity and Emerging Technologies',
                                  style={'color': 'gray'}),
                        html.Br(),
                        html.Span('Advanced Research Institute for Informatics, Networking and Computing',
                                  style={'color': 'gray'}),
                        html.Br(),
                        html.Span('De La Salle University',
                                  style={'color': 'gray'}),
                    ]),
                ]),

                html.Br(),

                html.H4('Partner Industry', className='pb-1'),
                html.Ul([
                    html.Li([
                        'Senti Techlabs Inc.',
                    ])
                ]),

                html.Br(),

                html.H4('Funding Agency', className='pb-1'),
                html.Ul([
                    html.Li([
                        'Department of Science and Technology – Philippine Council for Industry, Energy and Emerging Technology Research and Development (DOST-PCIEERD)',
                    ])
                ]),

                html.Br(),

                html.H4('Data Engineers', className='pb-1'),
                html.Ul([
                    html.Li('Daryll Tumambing'),
                    html.Li('Dennis Diego')
                ]),

                html.Br(),

                html.H4('Research Assistants', className='pb-1'),
                html.Ul([
                    html.Li('Mark Edward Gonzales'),
                    html.Li('James Kevin Lin'),
                    html.Li('Phoebe Clare Ong'),
                    html.Li('Criscela Ysabelle Racelis'),
                    html.Li('Sharmaine Gaw'),
                    html.Li('Christine Deticio'),
                    html.Li('Robi Jeanne Banogon'),
                    html.Li('Danielle Kirsten Sison'),
                    html.Li('Dan John Velasco'),
                    html.Li('Bryce Anthony Ramirez'),
                    html.Li('Trisha Gail Pelagio'),
                    html.Li('Axel Alba')
                ])

            ], width=9, className='px-0'),

            dbc.Col(width=3)
        ], style={'paddingTop': '2em',
                  'paddingBottom': '1.75em'}),
    ])

layout = dbc.Container([
    html.Br(),
    html.Br(),
    html.Br(),
    people,
])
