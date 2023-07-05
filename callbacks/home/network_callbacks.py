from dash import Input, Output, State
from dash.exceptions import PreventUpdate

import networkx as nx


def init_callback(app):
    @app.callback(
        Output('network', 'elements'),
        Input('search-word-submit-btn', 'n_clicks'),
        State('search-word', 'value'),
        Input('communities-dropdown', 'value')
    )
    def display_network(n_clicks, word, community_idx):
        if n_clicks >= 1:
            network = f'static/data/{word}/{community_idx}.tsv'
            G = nx.read_edgelist(network, data=(("coexpress",),))

            elements = nx.cytoscape_data(G)['elements']

            print(elements)

            return elements

        raise PreventUpdate
