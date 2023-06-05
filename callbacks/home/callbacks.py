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
                        sanitized_example_sentences = sanitize_example_sentences(
                            i, df)
                        example_sentences = []

                        for sentence in sanitized_example_sentences:
                            example_sentences.append(
                                html.Li(
                                    f'{sentence} (Sources)',
                                    style={'fontSize': '0.9em',
                                           'color': 'gray',
                                           'marginLeft': '1.5em'}
                                ),
                            )

                        def_list.append(html.Li([
                            html.Span(
                                df.loc[i, 'pos'],
                                style={'fontStyle': 'italic'}
                            ),
                            html.Br(),
                            html.Span(
                                'Definition lorem ipsum',
                                style={'fontSize': '0.9em',
                                       'marginLeft': '1.5em'}
                            ),
                            html.Br(),
                            html.Ul(example_sentences,
                                    id={
                                        'type': 'word-def-example-sentences-list',
                                        'index': i
                                    }),
                            html.Br(),
                            html.Span(
                                'See less sample sentences ▼',
                                style={'fontSize': '0.9em',
                                       'color': 'gray', 'marginLeft': '1.5em'},
                                id={
                                    'type': 'word-def-see-more-example-sentences-list',
                                    'index': i
                                }, n_clicks=0
                            )

                        ], style={'fontSize': '1.10em'}))

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
    def test(n_clicks):
        if n_clicks >= 1:
            if n_clicks % 2 == 0:
                return {'display': 'block'}, f'See less sample sentences ▼'

            return {'display': 'none'}, f'See more sample sentences ▼'

        raise PreventUpdate

    @app.callback(
        Output('checklist-sense', 'options'),
        Output('checklist-sense', 'value'),
        Input('search-word-submit-btn', 'n_clicks'),
        State('search-word', 'value')
    )
    def display_checklist_sense(n_clicks, word):
        if n_clicks >= 1:
            if word:
                df = get_definition_list(word)

                if len(df) >= 1:
                    return df['sense_id'].values, df['sense_id'].values
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
                fig = px.line(data[mask], x='year', y='counts', color='source')

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
                    df = get_definition_list(word)
                    data = convert_to_data_by_sense(
                        df['contextual_info'].values, df['sense_id'].values)

                    return data['source'].unique(), data['source'].unique()
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

                mask = data.source.isin(checklist_source)
                fig = px.line(data[mask], x='year',
                              y='counts', color='sense')

                return fig

            raise PreventUpdate

        raise PreventUpdate
