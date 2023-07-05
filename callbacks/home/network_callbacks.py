from dash import Input, Output, State
from plotly.graph_objs import *
from dash.exceptions import PreventUpdate
from .util import *
from .network_util import *


def init_callback(app):
    @app.callback(
        Output('network', 'elements'),
        Input('search-word-submit-btn', 'n_clicks'),
        State('search-word', 'value'),
        Input('communities-dropdown', 'value')
    )
    def display_network(n_clicks, word, community_idx):
        if n_clicks >= 1:
            df = get_definition_list(word)

            if len(df) >= 1:
                all_words = [(word, word)]
                edges = []
                for i in range(len(df)):
                    network = parse_json_communities(word, community_idx)

                    for j in network:
                        item = (word, j)
                        edges.append(item)

                        if j not in all_words:
                            item = (j, j)
                            all_words.append(item)

                nodes = [
                    {'data': {'id': identifier, 'label': label}}
                    for identifier, label in (
                        all_words
                    )
                ]

                edge_list = [
                    {'data': {'source': source, 'target': target}}
                    for source, target in (
                        edges
                    )
                ]
                elements = nodes + edge_list

                return elements

        raise PreventUpdate
