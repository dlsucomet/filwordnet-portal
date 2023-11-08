import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, State, html
from dash.exceptions import PreventUpdate
from plotly.graph_objs import *

from ..api_query import *
from ..sense.util import *
from .util import *


def init_callback(app, API_URL):
    @app.callback(
        Output('word-plot-sense', 'children'),
        Input('submitted-word', 'data'),
        Input('word-exists', 'data')
    )
    def display_word_in_the_sense_plot_description(word, word_exists):
        if word and word_exists:
            return [
                f' {word} ',
                html.I(className='bi bi-info-circle'),
                f' '
            ]

        raise PreventUpdate

    @app.callback(
        Output('word-plot-source', 'children'),
        Input('submitted-word', 'data'),
        Input('word-exists', 'data')
    )
    def display_word_in_the_source_plot_description(word, word_exists):
        if word and word_exists:
            return [
                f' {word} ',
                html.I(className='bi bi-info-circle'),
                f' '
            ]

        raise PreventUpdate

    @app.callback(
        Output('word-plot-modal', 'children'),
        Output('word-plot-modal', 'is_open'),
        Input('word-plot-source', 'n_clicks'),
        Input('word-plot-sense', 'n_clicks'),
        Input('word-plot-network', 'n_clicks'),
        State('submitted-word', 'data')
    )
    def display_word_tooltip_in_the_source_plot(source_n_clicks, sense_n_clicks, network_n_clicks, word):
        if source_n_clicks > 0 or sense_n_clicks > 0 or network_n_clicks > 0:
            df = get_word_db(API_URL, word)
            nlp_word_df = get_nlp_word(API_URL, word)

            sense_list = []
            sense_num = 0

            # netsci
            if len(df) >= 1:
                for i in range(len(df)):
                    sample_sentence_list = df.iloc[i]['example_sentences']

                    sentence = find_first_sample_sentence(sample_sentence_list)
                    start_idx = sentence.lower().find(word.lower())
                    sentence_before_word = sentence[:start_idx]
                    sentence_word = sentence[start_idx: start_idx +
                                             len(word)].strip()
                    sentence_after_word = sentence[start_idx +
                                                   len(word):]

                    if len(sentence_before_word) == 0:
                        sentence_word = capitalize_first_word(
                            sentence_word)

                    html_sample_sentence = html.Ul()
                    if len(sample_sentence_list) >= 1:
                        html_sample_sentence = html.Ul(
                            children=[
                                html.Li([
                                    html.Span('Sample Sentence: '),
                                    html.Span(
                                        capitalize_first_word(
                                            sentence_before_word),
                                        style={'color': 'gray'}
                                    ),
                                    html.Span(
                                        html.B(sanitize_symbols(
                                            sentence_word)),
                                        style={'color': 'gray'}
                                    ),
                                    html.Span(
                                        sanitize_symbols(sentence_after_word),
                                        style={'color': 'gray'}
                                    )
                                ])
                            ]
                        )

                    sense_num += 1

                    sense_list.append(
                        html.Li([
                            html.B(f'Sense {sense_num}'),
                            html_sample_sentence,
                            html.Br()
                        ])
                    )
            # nlp
            if len(nlp_word_df) >= 1:
                for i in range(len(nlp_word_df)):
                    sample_sentence_list = nlp_word_df.iloc[i]['example_sentences']

                    sentence = find_first_sample_sentence(sample_sentence_list)
                    start_idx = sentence.lower().find(word.lower())
                    sentence_before_word = sentence[:start_idx]
                    sentence_word = sentence[start_idx: start_idx +
                                             len(word)].strip()
                    sentence_after_word = sentence[start_idx +
                                                   len(word):]

                    if len(sentence_before_word) == 0:
                        sentence_word = capitalize_first_word(
                            sentence_word)

                    html_sample_sentence = html.Ul()
                    if len(sample_sentence_list) >= 1:
                        html_sample_sentence = html.Ul(
                            children=[
                                html.Li([
                                    html.Span('Sample Sentence: '),
                                    html.Span(
                                        capitalize_first_word(
                                            sentence_before_word),
                                        style={'color': 'gray'}
                                    ),
                                    html.Span(
                                        html.B(sanitize_symbols(
                                            sentence_word)),
                                        style={'color': 'gray'}
                                    ),
                                    html.Span(
                                        sanitize_symbols(sentence_after_word),
                                        style={'color': 'gray'}
                                    )
                                ])
                            ]
                        )

                    sense_num += 1

                    sense_list.append(
                        html.Li([
                            html.B(f'Sense {sense_num}'),
                            html_sample_sentence,
                            html.Br()
                        ])
                    )

            modal = [
                dbc.ModalHeader(
                    dbc.ModalTitle(word)
                ),
                dbc.ModalBody([
                    html.Ul([
                        html.Li([
                            s for s in sense_list
                        ])
                    ], className='mb-0')
                ])
            ]

            return modal, True

        raise PreventUpdate

    @app.callback(
        Output('sense-dropdown', 'options'),
        Output('sense-dropdown', 'value'),
        Input('submitted-word', 'data'),
        Input('word-exists', 'data')
    )
    def display_sense_dropdown(word, word_exists):
        if word and word_exists:
            df = get_word_db(API_URL, word)
            nlp_word_df = get_nlp_word(API_URL, word)

            checklist_options = {}
            num_sense = 0

            # netsci word
            if len(df) >= 1:
                for i in range(len(df)):
                    sense_id = df.iloc[i]['sense_id']

                    pos = ''
                    # if 'pos' in df.columns:
                    #    pos = df.iloc[i]['pos']

                    checklist_options[sense_id] = sense_and_pos_text(
                        f'Sense {num_sense+1}', pos)
                    num_sense = num_sense + 1

            # nlp word
            if len(nlp_word_df) >= 1:
                for i in range(len(nlp_word_df)):
                    sense_id = nlp_word_df.iloc[i]['sense_id']

                    pos = ''
                    # if 'pos' in nlp_word_df.columns:
                    #    pos = nlp_word_df.iloc[i]['pos']

                    checklist_options[sense_id] = sense_and_pos_text(
                        f'Sense {num_sense+1}', pos)
                    num_sense = num_sense + 1

            if len(df) >= 1 or len(nlp_word_df) >= 1:
                selected_option = None
                if not checklist_options:
                    checklist_options = {None: None}
                else:
                    selected_option = list(checklist_options.keys())[0]

                return checklist_options, selected_option

            else:
                # TODO: Handle case where word is not in database
                raise PreventUpdate

        raise PreventUpdate

    @app.callback(
        Output('sense-sample-sentence', 'children'),
        Input('sense-dropdown', 'value'),
        Input('submitted-word', 'data'),
        Input('word-exists', 'data')
    )
    def plot_update_sample_sentence_base_on_sense(sense_value, word, word_exists):

        if word and sense_value and word_exists:
            df = get_word_db(API_URL, word)  # get_definition_list(word)
            nlp_word_df = get_nlp_word(API_URL, word)

            if len(df) > 0:
                sense_id_df = df.loc[df['sense_id'] == sense_value.lower()]

                if len(sense_id_df) >= 1:
                    sample_sentence_list = sense_id_df.iloc[0]['example_sentences']

                    sentence = ''
                    if len(sample_sentence_list) > 0:
                        sentence = find_first_sample_sentence(
                            sample_sentence_list)

                        sentence = find_first_sample_sentence(
                            sample_sentence_list)
                        start_idx = sentence.lower().find(word.lower())
                        sentence_before_word = sentence[:start_idx]
                        sentence_word = sentence[start_idx: start_idx +
                                                 len(word)].strip()
                        sentence_after_word = sentence[start_idx +
                                                       len(word):]

                        if len(sentence_before_word) == 0:
                            sentence_word = capitalize_first_word(
                                sentence_word)

                    sense_data = html.Div(
                        children=[
                            html.Br(),
                            html.Div(
                                children=[
                                    html.Span('Sample Sentence: '),
                                    html.Span(
                                        capitalize_first_word(
                                            sentence_before_word),
                                        style={'color': 'gray'}
                                    ),
                                    html.Span(
                                        html.B(sanitize_symbols(
                                            sentence_word)),
                                        style={'color': 'gray'}
                                    ),
                                    html.Span(
                                        sanitize_symbols(sentence_after_word),
                                        style={'color': 'gray'}
                                    )
                                ]
                            )
                        ]
                    )
                    return sense_data

            if len(nlp_word_df) > 0:
                sense_id_df = nlp_word_df.loc[nlp_word_df['sense_id']
                                              == sense_value.lower()]

                if len(sense_id_df) >= 1:
                    sample_sentence_list = sense_id_df.iloc[0]['example_sentences']

                    sentence = ''
                    if len(sample_sentence_list) > 0:
                        sentence = find_first_sample_sentence(
                            sample_sentence_list)

                        sentence = find_first_sample_sentence(
                            sample_sentence_list)
                        start_idx = sentence.lower().find(word.lower())
                        sentence_before_word = sentence[:start_idx]
                        sentence_word = sentence[start_idx: start_idx +
                                                 len(word)].strip()
                        sentence_after_word = sentence[start_idx +
                                                       len(word):]

                        if len(sentence_before_word) == 0:
                            sentence_word = capitalize_first_word(
                                sentence_word)

                    sense_data = html.Div(
                        children=[
                            html.Br(),
                            html.Div(
                                children=[
                                    html.Span('Sample Sentence: '),
                                    html.Span(
                                        capitalize_first_word(
                                            sentence_before_word),
                                        style={'color': 'gray'}
                                    ),
                                    html.Span(
                                        html.B(sanitize_symbols(
                                            sentence_word)),
                                        style={'color': 'gray'}
                                    ),
                                    html.Span(
                                        sanitize_symbols(sentence_after_word),
                                        style={'color': 'gray'}
                                    )
                                ]
                            ),
                        ]
                    )
                    return sense_data

        raise PreventUpdate

    @app.callback(
        Output('graph-sense', 'figure'),
        Input('sense-dropdown', 'value'),
        Input('submitted-word', 'data'),
        Input('word-exists', 'data')
    )
    def update_line_chart(sense_value, word, word_exists):
        if word and word_exists:
            df = get_word_db(API_URL, word)
            nlp_word_df = get_nlp_word(API_URL, word)

            pos = ''
            if 'pos' in df.columns:
                pos = df['pos'].values

            data = convert_to_data_by_sense(
                df['contextual_info'].values, df['sense_id'].values, pos)
            nlp_data = convert_to_data_by_sense(
                nlp_word_df['contextual_info'].values, nlp_word_df['sense_id'].values, pos, nlp=True, offset=df['sense_id'].nunique())

            data = pd.concat([data, nlp_data])

            data = data.rename(columns={'category': 'Source',
                                        'year': 'Year',
                                        'sense_and_pos': 'Word Sense',
                                        'counts': 'Num. of Appearances'})

            data = data.groupby(['Source', 'Year', 'Word Sense', 'sense'])[
                'Num. of Appearances'].sum().reset_index()

            mask = data.sense.isin([sense_value])

            # https://github.com/plotly/plotly.py/issues/3441
            fig = go.Figure(layout=dict(template='plotly'))
            fig = px.line(data[mask], x='Year',
                          y='Num. of Appearances', color='Source', markers=True,
                          color_discrete_sequence=px.colors.qualitative.Safe)

            fig.update_xaxes(
                categoryorder='category ascending', linecolor='gray', tickangle=-45)
            fig.update_yaxes(linecolor='gray',
                             gridcolor='#D3D3D3', gridwidth=0.5)
            fig.update_layout(
                legend_title_text='Source',
                xaxis_title='Year',
                yaxis_title='Number of Appearances',
                plot_bgcolor='white'
            )

            return fig

        raise PreventUpdate

    @app.callback(
        Output('source-dropdown', 'options'),
        Output('source-dropdown', 'value'),
        Input('submitted-word', 'data'),
        Input('word-exists', 'data')
    )
    def display_source_dropdown(word, word_exists):
        if word and word_exists:
            df = get_word_db(API_URL, word)
            nlp_word_df = get_nlp_word(API_URL, word)

            pos = ''
            if 'pos' in df.columns:
                pos = df['pos'].values

            data = convert_to_data_by_sense(
                df['contextual_info'].values, df['sense_id'].values, pos)
            nlp_data = convert_to_data_by_sense(
                nlp_word_df['contextual_info'].values, nlp_word_df['sense_id'].values, pos, nlp=True)

            data = pd.concat([data, nlp_data])

            return data['category'].unique(), data['category'].unique()[0]

        raise PreventUpdate

    @app.callback(
        Output('graph-source', 'figure'),
        Input('source-dropdown', 'value'),
        Input('submitted-word', 'data'),
        Input('word-exists', 'data')
    )
    def update_line_chart(selected_source, word, word_exists):
        if word and word_exists:
            df = get_word_db(API_URL, word)
            nlp_word_df = get_nlp_word(API_URL, word)

            pos = ''
            if 'pos' in df.columns:
                pos = df['pos'].values

            data = convert_to_data_by_sense(
                df['contextual_info'].values, df['sense_id'].values, pos)
            nlp_data = convert_to_data_by_sense(
                nlp_word_df['contextual_info'].values, nlp_word_df['sense_id'].values, pos, nlp=True, offset=df['sense_id'].nunique())

            data = pd.concat([data, nlp_data])

            data = data.rename(columns={'category': 'Source',
                                        'year': 'Year',
                                        'sense_and_pos': 'Word Sense',
                                        'counts': 'Num. of Appearances'})

            data = data.groupby(['Word Sense', 'sense', 'Year', 'Source'])[
                'Num. of Appearances'].sum().reset_index()

            mask = data.Source.isin([selected_source])

            # https://github.com/plotly/plotly.py/issues/3441
            fig = go.Figure(layout=dict(template='plotly'))
            fig = px.line(data[mask], x='Year',
                          y='Num. of Appearances', color='Word Sense', markers=True,
                          color_discrete_sequence=px.colors.qualitative.Safe)

            fig.update_xaxes(
                categoryorder='category ascending', linecolor='gray', tickangle=-45)
            fig.update_yaxes(linecolor='gray',
                             gridcolor='#D3D3D3', gridwidth=0.5)
            fig.update_layout(
                legend_title_text='Word Sense',
                xaxis_title='Year',
                yaxis_title='Number of Appearances',
                plot_bgcolor='white'
            )

            return fig

        raise PreventUpdate
