from dash import Input, Output, State, html
import plotly.express as px
from dash.exceptions import PreventUpdate
from .util import *


def init_callback(app):
    @app.callback(
        Output('graph', 'figure'),
        Input('checklist', 'value')
    )
    def update_line_chart(continents):
        df = px.data.gapminder()  # replace with your own data source
        mask = df.continent.isin(continents)
        fig = px.line(df[mask],
                      x='year', y='lifeExp', color='country')
        return fig

    @app.callback(
        Output('graph1', 'figure'),
        Input('checklist1', 'value')
    )
    def update_line_chart1(continents):
        df = px.data.gapminder()  # replace with your own data source
        mask = df.continent.isin(continents)
        fig = px.line(df[mask],
                      x='year', y='lifeExp', color='country')
        return fig

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
                            html.Ul(example_sentences)

                        ], style={'fontSize': '1.10em'}))

                    return word, def_list
                else:
                    return [f'No Word Found: {word}'], None

            else:
                return [f'No Word Found: '], None

        raise PreventUpdate
