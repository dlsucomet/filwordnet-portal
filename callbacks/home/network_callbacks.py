from dash import Input, Output, State
from dash.exceptions import PreventUpdate

import networkx as nx

from .network_util import *


def init_callback(app):
    @app.callback(
        Output('communities-dropdown', 'options'),
        Input('search-word-submit-btn', 'n_clicks'),
        State('search-word', 'value')
    )
    def populate_communities_dropdown(n_clicks, word):
        if n_clicks >= 1:
            return [{'label': 'Community ' + str(i + 1), 'value': i} for i in range(get_num_communities(word))]

        raise PreventUpdate

    @app.callback(
        Output('network', 'elements'),
        Output('network', 'layout'),
        Input('search-word-submit-btn', 'n_clicks'),
        State('search-word', 'value'),
        Input('communities-dropdown', 'value'),
        Input('communities-layout', 'value')
    )
    def display_network(n_clicks, word, community_idx, layout):
        if n_clicks >= 1:
            network = f'static/data/{word}/{community_idx}.tsv'
            G = nx.read_edgelist(network)

            elements = nx.cytoscape_data(G)['elements']
            for node in elements['nodes']:
                if node['data']['id'] == word:
                    node['classes'] = 'shaded'

            return elements, {'name': layout}

        raise PreventUpdate
