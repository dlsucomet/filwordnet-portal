from dash import Input, Output, State, html, Patch, MATCH
import plotly.express as px
from dash.exceptions import PreventUpdate
from .util import *


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
                        example_sentences_list = sanitize_example_sentences(
                            i, df)

                        html_example_sentences_list = []
                        for sentence in example_sentences_list:
                            item = html.Div([
                                html.Span(f'{sentence} (Source)'),
                                html.Br()
                            ])

                            html_example_sentences_list.append(item)

                        def_list.append(html.Tr([
                            html.Td(
                                html.Span(f'Sense #{i+1}:'),
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
                                    html.Ol([
                                        html.Li(
                                            html.Span(
                                                html_example_sentences_list[0]
                                            )
                                        ),
                                        html.Div(children=[html.Li(i) for i in html_example_sentences_list[1:]],
                                                 id={
                                            'type': 'word-def-example-sentences-list',
                                            'index': i
                                        },
                                            style={'display': 'none'}),

                                    ], style={'fontSize': '0.9em',
                                              'color': 'gray',
                                              'list-style-type': 'lower-alpha'
                                              }),
                                    html.Span(
                                        'See more sample sentences ▼',
                                        style={'fontSize': '0.9em',
                                               'color': 'gray'},
                                        className='see-more',
                                        id={
                                            'type': 'word-def-see-more-example-sentences-list',
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
        Output({'type': 'word-def-example-sentences-list',
               'index': MATCH}, 'style'),
        Output({'type': 'word-def-see-more-example-sentences-list',
                'index': MATCH}, 'children'),
        Input({'type': 'word-def-see-more-example-sentences-list',
              'index': MATCH}, 'n_clicks')
    )
    def see_or_hide_more_sentences(n_clicks):
        if n_clicks >= 1:
            if n_clicks % 2 == 0:
                return {'display': 'block'}, f'See less sample sentences ▲'

            return {'display': 'none'}, f'See more sample sentences ▼'

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
        Output('checklist-sense', 'options'),
        Output('checklist-sense', 'value'),
        Output('embeddings-checklist', 'options'),
        Output('embeddings-checklist', 'value'),
        Input('search-word-submit-btn', 'n_clicks'),
        State('search-word', 'value')
    )
    def display_checklist_sense(n_clicks, word):
        if n_clicks >= 1:
            if word:
                df = get_definition_list(word)

                if len(df) >= 1:
                    return df['sense_id'].values, df['sense_id'].values, df['sense_id'].values, df['sense_id'].values
                else:
                    # TODO: Handle case where word is not in database
                    raise PreventUpdate

            raise PreventUpdate

        raise PreventUpdate

    @app.callback(
        Output('graph-sense', 'figure'),
        Input('checklist-sense', 'value'),
        Input('search-word-submit-btn', 'n_clicks'),
        State('search-word', 'value')
    )
    def update_line_chart(checklist_sense, n_clicks, word):
        if n_clicks >= 1:
            if word:
                df = get_definition_list(word)
                data = convert_to_data_by_sense(
                    df['contextual_info'].values, df['sense_id'].values)

                mask = data.sense.isin(checklist_sense)
                fig = px.line(data[mask], x='year', y='counts', color='category')

                fig.update_xaxes(categoryorder='category ascending')

                return fig

            raise PreventUpdate

        raise PreventUpdate

    @app.callback(
        Output('checklist-source', 'options'),
        Output('checklist-source', 'value'),
        Input('search-word-submit-btn', 'n_clicks'),
        State('search-word', 'value')
    )
    def display_checklist_sense(n_clicks, word):
        if n_clicks >= 1:
            if word:
                df = get_definition_list(word)

                if len(df) >= 1:

                    data = convert_to_data_by_sense(
                        df['contextual_info'].values, df['sense_id'].values)

                    return data['category'].unique(), data['category'].unique()
                else:
                    # TODO: Handle case where word is not in database
                    raise PreventUpdate

            raise PreventUpdate

        raise PreventUpdate

    @app.callback(
        Output('graph-source', 'figure'),
        Input('checklist-source', 'value'),
        Input('search-word-submit-btn', 'n_clicks'),
        State('search-word', 'value')
    )
    def update_line_chart(checklist_source, n_clicks, word):
        if n_clicks >= 1:
            if word:
                df = get_definition_list(word)
                data = convert_to_data_by_sense(
                    df['contextual_info'].values, df['sense_id'].values)

                mask = data.category.isin(checklist_source)
                fig = px.line(data[mask], x='year',
                              y='counts', color='sense')

                fig.update_xaxes(categoryorder='category ascending')

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
            if len(df) >= 1:
                embeddings_list = []
                for i in range(len(df)):
                    embeddings = df.loc[i, 'sense_embedding']
                    embeddings = sanitize_embeddings(embeddings)
                    if embeddings:
                        embeddings_list.append(embeddings)

                components = load_embeddings(embeddings_list)
                fig = px.scatter_3d(components,
                                    x=0, y=1, z=2,
                                    color=df['sense_id'].values)
                return fig
        raise PreventUpdate
