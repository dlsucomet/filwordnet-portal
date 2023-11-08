from dash import ALL, Input, Output, ctx, html
from dash.exceptions import PreventUpdate
from plotly.graph_objs import *

from ..api_query import *
from ..plot.util import *
from ..sense.util import *
from .util import *


def init_callback(app, API_URL):
    @app.callback(
        Output('communities-dropdown', 'options'),
        Output('communities-dropdown', 'value'),
        Input('submitted-word', 'data'),
        Input('word-exists', 'data')
    )
    def populate_communities_dropdown(word, word_exists):
        if word and word_exists:
            return [{'label': 'Sense ' + str(i + 1), 'value': i}
                    for i in range(get_num_senses(API_URL, word) + get_num_nlp_senses(API_URL, word))], 0

        raise PreventUpdate

    @app.callback(
        Output('input-word-network', 'children'),
        Input('submitted-word', 'data'),
        Input('word-exists', 'data')
    )
    def search_word(word, word_exists):
        if word and word_exists:
            df = get_word_db(API_URL, word)
            if len(df) >= 1:
                return word

        raise PreventUpdate

    @app.callback(
        Output('network-cooccurring-words', 'children'),
        Input('submitted-word', 'data'),
        Input('communities-dropdown', 'value'),
        Input('word-exists', 'data')
    )
    def display_co_occurring_words(word, sense_id, word_exists):
        if word_exists:
            netsci_df = get_netsci_word(API_URL, word)
            try:
                if sense_id >= len(netsci_df):
                    return html.Div('Data processing is ongoing for this sense',
                                    style={'color': 'gray'})
            except:
                pass

            word_list = get_word_list_db(API_URL)
            for entry in netsci_df:
                if entry['sense_id'] == f'ns_{word}_{sense_id}':
                    existing_words = []
                    non_existing_words = []
                    for cooccurring_word in entry['community']:
                        if cooccurring_word in word_list:
                            existing_words.append(html.Span(
                                cooccurring_word, className='link-primary',
                                n_clicks=0,
                                id={'type': 'co-occurring-word',
                                    'index': cooccurring_word},
                                style={'text-decoration': 'none'}))

                        else:
                            non_existing_words.append(
                                html.Span(cooccurring_word))

                    ret_val = []
                    for cooccurring_word in existing_words:
                        ret_val.append(cooccurring_word)
                        ret_val.append(html.Span(' ', className='me-2'))

                    non_existing_ret_val = []
                    for cooccurring_word in non_existing_words:
                        non_existing_ret_val.append(cooccurring_word)
                        non_existing_ret_val.append(
                            html.Span(' ', className='me-2'))

                    if non_existing_ret_val:
                        if ret_val:
                            return html.Div([html.Div(ret_val), html.Br(),
                                             html.B(
                                                 'More Co-Occurring Words:'),
                                             html.Div(non_existing_ret_val, className='mt-3')])

                        return html.Div([html.Div(non_existing_ret_val, className='mt-3')])

                    return html.Div([html.Div(ret_val)])

        raise PreventUpdate

    @app.callback(
        Output('search-word', 'value', allow_duplicate=True),
        Output('search-word-submit-btn', 'n_clicks', allow_duplicate=True),
        Input({'type': 'co-occurring-word',
               'index': ALL}, 'n_clicks'),
        prevent_initial_call=True
    )
    def select_co_occurring_word(n_clicks):
        try:
            if 1 in n_clicks:
                return ctx.triggered_id['index'], 1
        except:
            raise PreventUpdate

        raise PreventUpdate

    @app.callback(
        Output('network-sample-sentence', 'children'),
        Input('communities-dropdown', 'value'),
        Input('submitted-word', 'data'),
        Input('word-exists', 'data')
    )
    def plot_update_sample_sentence_base_on_sense(sense_value, word, word_exists):
        if word and word_exists:
            df = get_word_db(API_URL, word)  # get_definition_list(word)
            nlp_word_df = get_nlp_word(API_URL, word)

            if len(df) > 0 and sense_value < len(df):
                sense_id_df = df.iloc[[sense_value]]

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
                sense_id_df = nlp_word_df.iloc[[sense_value - len(df)]]

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
