from dash import Input, Output, State
from dash.exceptions import PreventUpdate

def init_callback(app):
    @app.callback(
        Output('home-body-container', 'hidden'),
        Output('home-sidebar', 'hidden'),
        Output('submitted-word', 'data'),
        Input('search-word-submit-btn', 'n_clicks'),
        Input('search-word', 'n_submit'),
        State('search-word', 'value')
    )
    def submit_input(n_clicks, n_submit, word):
        if n_clicks >= 1 or n_submit >= 1:
            return False, False, word.lower() 

        raise PreventUpdate


