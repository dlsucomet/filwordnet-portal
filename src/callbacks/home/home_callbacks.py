from dash import ALL, Input, Output, State, ctx, html
from dash.exceptions import PreventUpdate
from strsimpy.jaro_winkler import JaroWinkler

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
                word = word.lower()

                netsci_word_df = get_word_db(API_URL, word)
                nlp_word_df = get_nlp_word(API_URL, word)

                if len(netsci_word_df) >= 1 or len(nlp_word_df) >= 1:
                    return False, False, word.lower(), '', True, True

                else:
                    # Get suggested words
                    words = get_word_list_db(API_URL)
                    jarowinkler = JaroWinkler()
                    suggestions = []

                    for candidate_word in words:
                        distance = 1 - jarowinkler.similarity(
                            candidate_word, word)
                        suggestions.append((distance, candidate_word))

                    MAX_NUM_SUGGESTIONS = 5
                    suggestions = [html.Span(suggestion[1],  className='link-primary me-2',
                                             n_clicks=0,
                                             id={'type': 'suggestion-word',
                                                 'index': suggestion[1]},
                                             style={'text-decoration': 'none'}) for suggestion in sorted(
                        suggestions)[:MAX_NUM_SUGGESTIONS]]

                    return True, True, word.lower(), [html.P(f'"{word}" is not in our database'),
                                                      html.Div([html.Span(
                                                          'Here are some suggested words:', className='me-2')] +
                                                          suggestions)], False, False

        raise PreventUpdate

    @app.callback(
        Output('search-word', 'value', allow_duplicate=True),
        Output('search-word-submit-btn', 'n_clicks', allow_duplicate=True),
        Input({'type': 'suggestion-word',
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
