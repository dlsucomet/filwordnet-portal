import dash_bootstrap_components as dbc
from dash import MATCH, Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate
from plotly.graph_objs import *

from ..api_query import *
from .util import *


def init_callback(app, API_URL):
    @app.callback(
        Output('senses-word', 'children'),
        Input('submitted-word', 'data'),
        Input('word-exists', 'data')
    )
    def search_word(word, word_exists):
        if word and word_exists:
            return word

        raise PreventUpdate

    @app.callback(
        Output('senses-container', 'children'),
        Input('submitted-word', 'data'),
        Input('word-exists', 'data')
    )
    def get_senses(word, word_exists):
        if word and word_exists:
            netsci_word_df = get_word_db(API_URL, word)
            nlp_word_df = get_nlp_word(API_URL, word)

            df = pd.concat([netsci_word_df, nlp_word_df])

            if len(df) >= 1:
                def_list = []
                for i in range(len(df)):
                    sample_sentences_list = df.iloc[i]['example_sentences']

                    html_sample_sentences_list = []
                    letter_bullet = ord('a')
                    for sentence in sample_sentences_list:
                        if is_quality_sentence(sentence):
                            start_idx = sentence.lower().find(word.lower())
                            sentence_before_word = sentence[:start_idx]
                            sentence_word = sentence[start_idx: start_idx +
                                                     len(word)].strip()
                            sentence_after_word = sentence[start_idx +
                                                           len(word):]

                            item = html.Tr([
                                html.Td(children=[
                                    html.Div(children=[
                                        f'{chr(letter_bullet)}. ',
                                    ])
                                ]),

                                html.Td(
                                    children=html.Div([
                                        sentence_before_word,
                                        html.B(sentence_word),
                                        sentence_after_word
                                    ])
                                )],
                                style={'fontSize': '0.9em',
                                       'color': 'gray',
                                       'verticalAlign': 'top'}
                            )

                            html_sample_sentences_list.append(item)
                            letter_bullet += 1

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
                        html_sample_sentences_container = html.Div([
                            html.Span(
                                'Sample Sentences',
                                style={'fontSize': '0.9em',
                                       'color': 'gray'}
                            ),

                            html.Div(
                                children=[
                                    dcc.Loading(
                                        dbc.Table(
                                            id={'type': 'senses-sample-sentences-hidden-container',
                                                'index': i},
                                            children=[
                                                html_sample_sentences_list[0]
                                            ],
                                            borderless=True,
                                            style={'marginBottom': '0'}
                                        )
                                    ),
                                    dbc.Table(
                                        id={'type': 'senses-sample-sentences-container',
                                            'index': i},
                                        children=[
                                            j for j in html_sample_sentences_list[1:]
                                        ], className='sample-sentence',
                                        borderless=True,
                                        style={'marginBottom': '0', 'display': 'none'})
                                ]
                            ),
                            html_see_more_text,
                            html.Br()
                        ])

                    html_pos = html.Div(
                        children=[
                            html.Br()
                        ]
                    )
                    if 'pos' in df.columns:
                        pos = display_pos(df.iloc[i]['pos'])
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
                            html.Div(f'Sense {i+1}:'),
                            style={'width': '11%'}),
                        html.Td(
                            html.Div([
                                html_sample_sentences_container,
                            ])
                        )], className='align-baseline')
                    )

                return def_list

            else:
                return None

        raise PreventUpdate

    @app.callback(
        Output({'type': 'senses-sample-sentences-hidden-container',
               'index': MATCH}, 'className'),
        Output({'type': 'senses-sample-sentences-container',
               'index': MATCH}, 'className'),
        Output({'type': 'senses-sample-sentences-container',
               'index': MATCH}, 'style'),
        Output({'type': 'word-def-see-more-sample-sentences-text',
                'index': MATCH}, 'children'),
        Input({'type': 'word-def-see-more-sample-sentences-text',
              'index': MATCH}, 'n_clicks')
    )
    def see_or_hide_more_sentences(n_clicks):
        if n_clicks % 2 == 1:
            return 'sample-sentence', 'sample-sentence-see-all', {'display': 'block'},  f'See less sample sentences ▲'

        return 'sample-sentence', 'sample-sentence', {'marginBottom': '0', 'display': 'none'}, f'See more sample sentences ▼'
