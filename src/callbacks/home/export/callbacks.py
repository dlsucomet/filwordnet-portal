from dash import Input, Output, dcc
from plotly.graph_objs import *
from dash.exceptions import PreventUpdate
from ..api_query import *
from .util import *


def init_callback(app, API_URL):
    @app.callback(
        Output('download-embeddings', 'data'),
        Input('submitted-word', 'data'),
        Input('export-embeddings', 'n_clicks')
    )
    def download_lift_over_table_to_csv(word, export_embeddings):
        if export_embeddings >= 1:
            df = pd.DataFrame(get_all_embeddings(API_URL, word))
            return dcc.send_data_frame(df.to_csv, f'{word}-embeddings.csv', index=False)

        raise PreventUpdate
