from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from .api_query import *

def init_callback(app, API_URL):
    @app.callback(
        Output('home-body-container', 'hidden'),
        Output('home-sidebar', 'hidden'),
        Output('submitted-word', 'data'),

        Output('search-word-error', 'children'),
        Output('search-word-error-container', 'hidden'),

        Output('word-exists', 'data'),

        Input('search-word-submit-btn', 'n_clicks'),
        Input('search-word', 'n_submit'),
        State('search-word', 'value')
    )
    def submit_input(n_clicks, n_submit, word):
        if n_clicks >= 1 or n_submit >= 1:
            if word:
                netsci_word_df = get_word_db(API_URL, word)
                nlp_word_df = get_nlp_word(API_URL, word)
                # print(df['example_sentences'])
            
                if len(netsci_word_df) >= 1 or len(nlp_word_df) >= 1:
                    return False, False, word.lower(), '', True, True
            
                else: 
                    #all_word = get_word_list_db(API_URL)
                    #print(all_word)
                    return True, True, word.lower(), [f'No Word Found: {word}'], False, False

        raise PreventUpdate


