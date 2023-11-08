import plotly.express as px
from dash import Input, Output
from dash.exceptions import PreventUpdate
from plotly.graph_objs import *

from ..api_query import *
from ..sense.util import *
from .util import *


def init_callback(app, API_URL):
    @app.callback(
        Output('embeddings', 'figure'),
        Input('submitted-word', 'data'),
        Input('word-exists', 'data')
    )
    def display_embeddings(word, word_exists):
        if word and word_exists:
            netsci_word_df = get_word_db(API_URL, word)
            df = get_word_embeddings_db(API_URL, word)

            sense_id_list = []
            sense_num = 0
            pca_embeddings_list = []

            if len(netsci_word_df) >= 1:
                for i in range(len(netsci_word_df)):
                    sense_num += 1
                    pca_embeddings_list.append([])
                    sense_id_list.append(f'Sense {sense_num}*')

            if len(df) >= 1:
                for i in range(len(df)):
                    sense_id = df.iloc[i]['sense_id']
                    pca_embeddings = get_pca_embeddings(API_URL, sense_id)

                    if pca_embeddings:
                        sense_num += 1
                        pca_embeddings_list.append(pca_embeddings)
                        sense_id_list.append(f'Sense {sense_num}')

                components = pd.DataFrame(pca_embeddings_list)
                components = components.rename(
                    columns={0: 'Component 1', 1: 'Component 2', 2: 'Component 3'})

                fig = px.scatter_3d(components,
                                    x='Component 1', y='Component 2', z='Component 3',
                                    color=sense_id_list,
                                    color_discrete_sequence=px.colors.qualitative.Safe)
                camera = dict(
                    eye=dict(x=1.75, y=1.75, z=1)
                )

                fig.update_layout(legend_title_text='Word Sense',
                                  scene=dict(
                                      xaxis=dict(
                                          zerolinecolor='gray',
                                          linecolor='gray',
                                          gridcolor='#D3D3D3',
                                          title='Component 1',
                                          showbackground=False
                                      ),
                                      yaxis=dict(
                                          zerolinecolor='gray',
                                          linecolor='gray',
                                          gridcolor='#D3D3D3',
                                          title='Component 2',
                                          showbackground=False
                                      ),
                                      zaxis=dict(
                                          zerolinecolor='gray',
                                          linecolor='gray',
                                          gridcolor='#D3D3D3',
                                          title='Component 3',
                                          showbackground=False
                                      )),
                                  scene_camera=camera
                                  )
                return fig

            else:
                # TODO: add exception handling
                raise PreventUpdate
        raise PreventUpdate

    @app.callback(
        Output('input-word-embeddings', 'children'),
        Input('submitted-word', 'data'),
        Input('word-exists', 'data')
    )
    def search_word(word, word_exists):
        if word and word_exists:
            df = get_word_db(API_URL, word)
            if len(df) >= 1:
                return word

        raise PreventUpdate
