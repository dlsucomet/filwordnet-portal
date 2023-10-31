from dash import Input, Output, html
from plotly.graph_objs import *
from dash.exceptions import PreventUpdate
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
            return [{'label': 'Sense ' + str(i + 1), 'value': i} for i in range(get_num_senses(API_URL, word))], 0

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

            return [f'No Word Found: {word}']

        raise PreventUpdate

    @app.callback(
        Output('network-cooccurring-words', 'children'),
        Input('submitted-word', 'data'),
        Input('communities-dropdown', 'value'),
        Input('word-exists', 'data')
    )
    def display_co_occurring_words(word, sense_id, word_exists):
        if word_exists:
            for entry in get_netsci_word(API_URL, word):
                if entry['sense_id'] == f'ns_{word}_{sense_id}':
                    cooccurring_words = [html.Span(cooccurring_word, className='link-primary', style={'text-decoration': 'none'})
                                        for cooccurring_word in entry['community']]

                    ret_val = []
                    for cooccurring_word in cooccurring_words:
                        ret_val.append(cooccurring_word)
                        ret_val.append(html.Span(' ', className='me-2'))

                    return ret_val
        
        raise PreventUpdate
