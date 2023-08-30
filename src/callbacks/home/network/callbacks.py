from dash import Input, Output
from plotly.graph_objs import *
from dash.exceptions import PreventUpdate
from ..api_query import *
from .util import *


def init_callback(app, API_URL):
    @app.callback(
        Output('input-word-network', 'children'),
        Input('submitted-word', 'data')
    )
    def search_word(word):
        if word:
            df = get_word_db(API_URL, word)

            if len(df) >= 1:
                return word

            return [f'No Word Found: {word}']

        raise PreventUpdate
