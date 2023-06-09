from dash import Input, Output, State, html, Patch, MATCH
from plotly.graph_objs import *
from dash.exceptions import PreventUpdate
from .util import *
from .sense_util import *
import dash_bootstrap_components as dbc


def init_callback(app):
    @app.callback(
        Output('submitted-word', 'data'),
        Input('search-word-submit-btn', 'n_clicks'),
        State('search-word', 'value')
    )
    def submit_input(n_clicks, word):
        if n_clicks >= 1:
            return word.lower()
        
        raise PreventUpdate

    @app.callback(
        Output('senses-word', 'children'),
        Output('senses-container', 'children'),
        Input('submitted-word', 'data')
    )
    def search_word(word):
        if word:
            df = get_definition_list(word)

            if len(df) >= 1:
                def_list = []
                for i in range(len(df)):
                    sample_sentences_list = sanitize_sample_sentences(
                        i, df)

                    html_sample_sentences_list = []
                    for sentence in sample_sentences_list:
                        item = html.Tr([
                            html.Td(children=[
                                html.Div(children=[
                                    f'Source'
                                ])
                            ],
                            ),

                            html.Td(children=[
                                html.Div(children=[
                                    f'{sentence}'
                                ])
                            ]
                            ),
                        ], style={'fontSize': '0.9em',
                                    'color': 'gray',
                                    'verticalAlign': 'top'})

                        html_sample_sentences_list.append(item)

                    html_see_more_text = html.Div()
                    if len(html_sample_sentences_list) >= 2:
                        html_see_more_text = html.Div(
                            children=[
                                'See more sample sentences ▼'
                            ],
                            style={'fontSize': '0.9em',
                                    'color': 'gray'},
                            className='see-more',
                            id={
                                'type': 'word-def-see-more-sample-sentences-text',
                                'index': i
                            }, n_clicks=0
                        )

                    html_sample_sentences_container = html.Div()
                    if len(html_sample_sentences_list) >= 1:
                        html_sample_sentences_container = html.Div(
                            children=[
                                html.Span('Sample Sentences',
                                            style={'fontSize': '0.9em',
                                                    'color': 'gray'}),
                                html.Br(),

                                dbc.Table(
                                    id={'type': 'senses-sample-sentences-container',
                                        'index': i},
                                    children=[
                                        j for j in html_sample_sentences_list
                                    ], className='sample-sentence',
                                    borderless=True,
                                    style={'marginBottom': '0'}),
                                html_see_more_text,
                                html.Br()
                            ]

                        )

                    html_pos = html.Div(
                        children=[
                            html.Br()
                        ]
                    )
                    pos = display_pos(df.loc[i, 'pos'])
                    if pos:
                        html_pos = html.Div(
                            children=[
                                html.Span(
                                    pos,
                                    style={'fontSize': '0.9em',
                                            'color': 'gray'}
                                ),
                                html.Br(),
                                html.Br()
                            ]
                        )

                    def_list.append(html.Tr([
                        html.Td(
                            html.Span(f'Sense {i+1}:'),
                            style={'width': '11%'}),
                        html.Td(
                            html.Div([
                                html.Span(
                                    'Definition lorem ipsum',
                                    style={'fontSize': '0.9em'}
                                ),
                                html_pos,

                                html_sample_sentences_container,

                            ]))], className='align-baseline'))

                patched_children = Patch()
                patched_children.append(def_list)

                return word, def_list

            else:
                return [f'No Word Found: {word}'], None

        raise PreventUpdate

    @app.callback(
        Output({'type': 'senses-sample-sentences-container',
               'index': MATCH}, 'className'),
        Output({'type': 'word-def-see-more-sample-sentences-text',
                'index': MATCH}, 'children'),
        Input({'type': 'word-def-see-more-sample-sentences-text',
              'index': MATCH}, 'n_clicks')
    )
    def see_or_hide_more_sentences(n_clicks):
        if n_clicks >= 1:
            if n_clicks % 2 == 0:
                return 'sample-sentence-see-all', f'See less sample sentences ▲'

            return 'sample-sentence', f'See more sample sentences ▼'

        raise PreventUpdate
