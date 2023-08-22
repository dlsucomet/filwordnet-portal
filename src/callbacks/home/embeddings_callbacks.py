from dash import Input, Output, State
import plotly.express as px
from plotly.graph_objs import *
from dash.exceptions import PreventUpdate
from .util import *
from .embeddings_util import *
from .sense_util import *


def init_callback(app, API_URL):
    @app.callback(
        Output('embeddings', 'figure'),
        Input('submitted-word', 'data')
    )
    def display_embeddings(word):
        if word:
            df = get_word_embeddings_db(API_URL, word) #get_definition_list(word)
            sense_id_list = []

            if len(df) >= 1:
                embeddings_list = []
                for i in range(len(df)):
                    embeddings = df.iloc[i]['sense_embedding']
                    embeddings = sanitize_embeddings(embeddings)
                    if embeddings:
                        embeddings_list.append(embeddings)
                        
                        #pos_abbrev, pos = sanitize_pos(df.loc[i, 'pos'])
                        #sense_id_list.append(f'Sense {i+1} ({pos})')
                        sense_id_list.append(f'Sense {i+1}')

                if len(embeddings_list) >= 3:
                    components = load_embeddings(embeddings_list)
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
