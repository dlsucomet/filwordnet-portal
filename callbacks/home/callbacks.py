from dash import Input, Output, State, html, Patch, MATCH
import plotly.express as px
from dash.exceptions import PreventUpdate
from .util import *
import dash_bootstrap_components as dbc


def init_callback(app):
    @app.callback(
        Output('senses-word', 'children'),
        Output('senses-container', 'children'),
        Input('search-word-submit-btn', 'n_clicks'),
        State('search-word', 'value')
    )
    def search_word(n_clicks, word):
        if n_clicks >= 1:
            if word:
                df = get_definition_list(word)

                if len(df) >= 1:
                    def_list = []
                    for i in range(len(df)):
                        sample_sentences_list = sanitize_sample_sentences(
                            i, df)

                        html_sample_sentences_list = []
                        for sentence in sample_sentences_list:
                            item = html.Tr([
                                html.Td(children=[
                                    html.Div(children=[
                                        f'Source'
                                    ])
                                ],
                                ),

                                html.Td(children=[
                                    html.Div(children=[
                                        f'{sentence}'
                                    ])
                                ]
                                ),
                            ], style={'fontSize': '0.9em',
                                      'color': 'gray'})

                            html_sample_sentences_list.append(item)

                        def_list.append(html.Tr([
                            html.Td(
                                html.Span(f'Sense {i+1}:'),
                                style={'width': '11%'}),
                            html.Td(
                                html.Div([
                                    html.Span(
                                        'Definition lorem ipsum',
                                        style={'fontSize': '0.9em'}
                                    ),
                                    html.Br(),
                                    html.Span(
                                        display_pos(df.loc[i, 'pos']),
                                        style={'fontSize': '0.9em',
                                               'color': 'gray'}
                                    ),
                                    html.Br(),
                                    html.Br(),
                                    html.Span(
                                        'Sample Sentences',
                                        style={'fontSize': '0.9em'}
                                    ),
                                    html.Br(),

                                    dbc.Table(
                                        id={'type': 'senses-sample-sentences-container',
                                            'index': i},
                                        children=[
                                            j for j in html_sample_sentences_list
                                        ], className='sample-sentence',
                                        borderless=True,
                                        style={'margin-bottom': '0'}),
                                    html.Span(
                                        'See more sample sentences ▼',
                                        style={'fontSize': '0.9em',
                                               'color': 'gray'},
                                        className='see-more',
                                        id={
                                            'type': 'word-def-see-more-sample-sentences-text',
                                            'index': i
                                        }, n_clicks=0
                                    ),
                                    html.Br(),
                                    html.Br()
                                ]))], className='align-baseline'))

                    patched_children = Patch()
                    patched_children.append(def_list)

                    return word, def_list

                else:
                    return [f'No Word Found: {word}'], None

            else:
                return [f'No Word Found: '], None

        raise PreventUpdate

    @app.callback(
        Output({'type': 'senses-sample-sentences-container',
               'index': MATCH}, 'className'),
        Output({'type': 'word-def-see-more-sample-sentences-text',
                'index': MATCH}, 'children'),
        Input({'type': 'word-def-see-more-sample-sentences-text',
              'index': MATCH}, 'n_clicks')
    )
    def see_or_hide_more_sentences(n_clicks):
        if n_clicks >= 1:
            if n_clicks % 2 == 0:
                return 'sample-sentence-see-all', f'See less sample sentences ▲'

            return 'sample-sentence', f'See more sample sentences ▼'

        raise PreventUpdate

    @app.callback(
        Output('network', 'elements'),
        Input('search-word-submit-btn', 'n_clicks'),
        State('search-word', 'value')
    )
    def display_network(n_clicks, word):
        if n_clicks >= 1:
            df = get_definition_list(word)

            if len(df) >= 1:
                all_words = [(word, word)]
                edges = []
                for i in range(len(df)):
                    network = df.loc[i, 'community']
                    network = sanitize_network_data(network)
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

    @app.callback(
        Output('sense-dropdown', 'options'),
        Output('sense-dropdown', 'value'),
        Input('search-word-submit-btn', 'n_clicks'),
        State('search-word', 'value')
    )
    def display_sense_dropdown(n_clicks, word):
        if n_clicks >= 1:
            if word:
                df = get_definition_list(word)

                if len(df) >= 1:

                    checklist_options = {}
                    num_sense = 0
                    for i in range(len(df)):
                        sense_id = df.loc[i, 'sense_id']
                        pos_abbrev, pos = sanitize_pos(df.loc[i, 'pos'])

                        checklist_options[sense_id] = f'Sense {num_sense+1} ({pos})'
                        num_sense = num_sense + 1

                    if not checklist_options:
                        checklist_options = {None: None}

                    return checklist_options, None
                else:
                    # TODO: Handle case where word is not in database
                    raise PreventUpdate

            raise PreventUpdate

        raise PreventUpdate

    @app.callback(
        Output('graph-sense', 'figure'),
        Input('sense-dropdown', 'value'),
        Input('search-word-submit-btn', 'n_clicks'),
        State('search-word', 'value')
    )
    def update_line_chart(sense_value, n_clicks, word):
        if n_clicks >= 1:
            if word:
                df = get_definition_list(word)
                data = convert_to_data_by_sense(
                    df['contextual_info'].values, df['sense_id'].values)

                mask = data.sense.isin([sense_value])
                fig = px.line(data[mask], x='year',
                              y='counts', color='category')

                fig.update_xaxes(categoryorder='category ascending')
                fig.update_layout(
                    xaxis_title='year',
                    yaxis_title='number of times it appeared'
                )

                return fig

            raise PreventUpdate

        raise PreventUpdate

    @app.callback(
        Output('source-dropdown', 'options'),
        Output('source-dropdown', 'value'),
        Input('search-word-submit-btn', 'n_clicks'),
        State('search-word', 'value')
    )
    def display_source_dropdown(n_clicks, word):
        if n_clicks >= 1:
            if word:
                df = get_definition_list(word)

                if len(df) >= 1:

                    data = convert_to_data_by_sense(
                        df['contextual_info'].values, df['sense_id'].values)

                    # data['category'].unique()
                    return data['category'].unique(), None
                else:
                    # TODO: Handle case where word is not in database
                    raise PreventUpdate

            raise PreventUpdate

        raise PreventUpdate

    @app.callback(
        Output('graph-source', 'figure'),
        Input('source-dropdown', 'value'),
        Input('search-word-submit-btn', 'n_clicks'),
        State('search-word', 'value')
    )
    def update_line_chart(selected_source, n_clicks, word):
        if n_clicks >= 1:
            if word:
                df = get_definition_list(word)
                data = convert_to_data_by_sense(
                    df['contextual_info'].values, df['sense_id'].values)

                mask = data.category.isin([selected_source])
                fig = px.line(data[mask], x='year',
                              y='counts', color='sense')

                fig.update_xaxes(categoryorder='category ascending')
                fig.update_layout(
                    xaxis_title='year',
                    yaxis_title='number of times it appeared'
                )

                return fig

            raise PreventUpdate

        raise PreventUpdate

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
                fig.update_layout(legend_title_text='Senses',
                                  scene=dict(
                                      xaxis_title='component 1',
                                      yaxis_title='component 2',
                                      zaxis_title='component 3')
                                  )
                return fig
        raise PreventUpdate
