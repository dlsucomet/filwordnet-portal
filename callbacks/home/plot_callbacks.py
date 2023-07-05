from dash import Input, Output, State
import plotly.express as px
from plotly.graph_objs import *
from dash.exceptions import PreventUpdate
from .util import *
from .plot_util import *


def init_callback(app):
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
                    df['contextual_info'].values, df['sense_id'].values, df['pos'].values)

                mask = data.sense.isin([sense_value])
                fig = px.line(data[mask], x='year',
                              y='counts', color='category')

                fig.update_xaxes(
                    categoryorder='category ascending', linecolor='black', tickangle=-45)
                fig.update_yaxes(linecolor='black',
                                 gridcolor='gray', gridwidth=0.5)
                fig.update_layout(
                    xaxis_title='Year',
                    yaxis_title='Number of Appearances',
                    plot_bgcolor='white'
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
                        df['contextual_info'].values, df['sense_id'].values, df['pos'].values)

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
                    df['contextual_info'].values, df['sense_id'].values, df['pos'].values)

                mask = data.category.isin([selected_source])
                fig = px.line(data[mask], x='year',
                              y='counts', color='sense_and_pos')

                fig.update_xaxes(
                    categoryorder='category ascending', linecolor='black', tickangle=-45)
                fig.update_yaxes(linecolor='black',
                                 gridcolor='gray', gridwidth=0.5)
                fig.update_layout(
                    xaxis_title='Year',
                    yaxis_title='Number of Appearances',
                    plot_bgcolor='white'
                )

                return fig

            raise PreventUpdate

        raise PreventUpdate
