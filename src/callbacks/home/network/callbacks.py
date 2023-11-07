from dash import ALL, Input, Output, ctx, html
from dash.exceptions import PreventUpdate
from plotly.graph_objs import *

from ..api_query import *
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
                                         html.B('More Co-Occurring Words:'),
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
