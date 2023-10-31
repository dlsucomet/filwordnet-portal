from dash import Input, Output
import plotly.express as px
from plotly.graph_objs import *
from dash.exceptions import PreventUpdate
from ..api_query import *
from .util import *
from ..sense.util import *


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

                components = pca_embeddings_list

                fig = px.scatter_3d(components,
                                    x=0, y=1, z=2,
                                    color=sense_id_list)
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
