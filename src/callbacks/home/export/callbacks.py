from dash import Input, Output, State, dcc
from dash.exceptions import PreventUpdate
from plotly.graph_objs import *

from ..api_query import *
from .util import *


def init_callback(app, API_URL):
    @app.callback(
        Output('download-embeddings', 'data'),
        State('submitted-word', 'data'),
        Input('export-embeddings', 'n_clicks'),
    )
    def download_lift_over_table_to_csv(word, export_embeddings):
        if export_embeddings >= 1:
            num_netsci_word = len(get_word_db(API_URL, word))
            num_nlp_word = len(get_nlp_word(API_URL, word))

            df = pd.DataFrame(get_all_embeddings(API_URL, word))
            df['sense'] = [i for i in range(
                num_netsci_word + 1, num_netsci_word + num_nlp_word + 1)]

            cols = list(df.columns.values)
            cols = [cols[-1]] + cols[1:]

            df = df[cols]

            return dcc.send_data_frame(df.to_csv, f'{word}-embeddings.csv', index=False)

        raise PreventUpdate

    @app.callback(
        Output('download-senses', 'data'),
        State('submitted-word', 'data'),
        Input('export-senses', 'n_clicks'),
    )
    def download_senses_to_json(word, export_embeddings):
        if export_embeddings >= 1:
            df = get_all_info(API_URL, word)

            return dict(content=df, filename=f'{word}.json')

        raise PreventUpdate
