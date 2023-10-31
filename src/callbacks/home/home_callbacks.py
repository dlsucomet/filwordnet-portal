from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from .api_query import *

def init_callback(app, API_URL):
    @app.callback(
        Output('home-body-container', 'hidden'),
        Output('home-sidebar', 'hidden'),
        Output('submitted-word', 'data'),

        Output('search-word-error', 'children'),
        Output('search-word-error', 'hidden'),

        Output('word-exists', 'data'),

        Input('search-word-submit-btn', 'n_clicks'),
        Input('search-word', 'n_submit'),
        State('search-word', 'value')
    )
    def submit_input(n_clicks, n_submit, word):
        if n_clicks >= 1 or n_submit >= 1:
            if word:
                df = get_word_db(API_URL, word)
     
                if len(df) >= 1:
                    return False, False, word.lower(), '', True, True
            
                else: 
                    return True, True, word.lower(), [f'No Word Found: {word}'], False, False

        raise PreventUpdate


