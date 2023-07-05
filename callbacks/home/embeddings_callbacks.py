from dash import Input, Output, State
import plotly.express as px
from plotly.graph_objs import *
from dash.exceptions import PreventUpdate
from .util import *
from .embeddings_util import *
from .sense_util import *


def init_callback(app):
    @app.callback(
        Output('embeddings', 'figure'),
        Input('embeddings-checklist', 'value'),
        Input('search-word-submit-btn', 'n_clicks'),
        State('search-word', 'value')
    )
    def display_embeddings(checklist_embeddings, n_clicks, word):
        if n_clicks >= 1:
            df = get_definition_list(word)
            sense_id_list = []

            if len(df) >= 1:
                embeddings_list = []
                for i in range(len(df)):
                    embeddings = df.loc[i, 'sense_embedding']
                    embeddings = sanitize_embeddings(embeddings)
                    if embeddings:
                        embeddings_list.append(embeddings)
                        pos_abbrev, pos = sanitize_pos(df.loc[i, 'pos'])
                        sense_id_list.append(f'Sense {i+1} ({pos})')

                components = load_embeddings(embeddings_list)
                fig = px.scatter_3d(components,
                                    x=0, y=1, z=2,
                                    color=sense_id_list)
                camera = dict(
                    eye=dict(x=1.75, y=1.75, z=1)
                )

                fig.update_layout(legend_title_text='Word Sense',
                                  scene=dict(
                                      xaxis_title='Component 1',
                                      yaxis_title='Component 2',
                                      zaxis_title='Component 3'),
                                  scene_camera=camera
                                  )
                # fig.update_traces(marker=dict(size=8)
                # line=dict(width=2,
                #          color='DarkSlateGrey')),
                # selector=dict(mode='markers')
                #                  )
                return fig
        raise PreventUpdate
