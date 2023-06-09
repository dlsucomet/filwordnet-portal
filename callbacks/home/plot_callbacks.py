from dash import Input, Output, State
import plotly.express as px
from plotly.graph_objs import *
from dash.exceptions import PreventUpdate
from .util import *
from .plot_util import *


def init_callback(app):
    @app.callback(
        Output('word-plot-sense', 'children'),
        Input('submitted-word', 'data')
    )
    def display_word_in_the_sense_plot_desciption(word):
        if word:
            return f' {word} '  

        raise PreventUpdate

    @app.callback(
        Output('word-plot-source', 'children'),
        Input('submitted-word', 'data')
    )
    def display_word_in_the_sense_plot_desciption(word):
        if word:
            return f' {word} '  

        raise PreventUpdate

    @app.callback(
        Output('sense-dropdown', 'options'),
        Output('sense-dropdown', 'value'),
        Input('submitted-word', 'data')
    )
    def display_sense_dropdown(word):
        if word:
            df = get_definition_list(word)

            if len(df) >= 1:

                checklist_options = {}
                num_sense = 0
                for i in range(len(df)):
                    sense_id = df.loc[i, 'sense_id']
                    
                    checklist_options[sense_id] = sense_and_pos_text(f'Sense {num_sense+1}', df.loc[i, 'pos'])
                    num_sense = num_sense + 1

                selected_option = None
                if not checklist_options:
                    checklist_options = {None: None}
                else:
                    selected_option = list(checklist_options.keys())[0]

                return checklist_options, selected_option
            else:
                # TODO: Handle case where word is not in database
                raise PreventUpdate

        raise PreventUpdate

    @app.callback(
        Output('graph-sense', 'figure'),
        Input('sense-dropdown', 'value'),
        Input('submitted-word', 'data')
    )
    def update_line_chart(sense_value, word):
        if word:
            df = get_definition_list(word)
            data = convert_to_data_by_sense(
                df['contextual_info'].values, df['sense_id'].values, df['pos'].values)

            data = data.groupby(['category', 'year', 'sense_and_pos', 'sense'])[
                'counts'].sum().reset_index()

            mask = data.sense.isin([sense_value])
            fig = px.line(data[mask], x='year',
                            y='counts', color='category', markers=True)

            fig.update_xaxes(
                categoryorder='category ascending', linecolor='gray', tickangle=-45)
            fig.update_yaxes(linecolor='gray',
                                gridcolor='#D3D3D3', gridwidth=0.5)
            fig.update_layout(
                legend_title_text='Source',
                xaxis_title='Year',
                yaxis_title='Number of Appearances',
                plot_bgcolor='white'
            )

            return fig

        raise PreventUpdate

    @app.callback(
        Output('source-dropdown', 'options'),
        Output('source-dropdown', 'value'),
        Input('submitted-word', 'data')
    )
    def display_source_dropdown(word):
        if word:
            df = get_definition_list(word)

            if len(df) >= 1:

                data = convert_to_data_by_sense(
                    df['contextual_info'].values, df['sense_id'].values, df['pos'].values)

                # data['category'].unique()
                return data['category'].unique(), data['category'].unique()[0]
            else:
                # TODO: Handle case where word is not in database
                raise PreventUpdate

        raise PreventUpdate

    @app.callback(
        Output('graph-source', 'figure'),
        Input('source-dropdown', 'value'),
        Input('submitted-word', 'data')
    )
    def update_line_chart(selected_source, word):
        if word:
            df = get_definition_list(word)
            data = convert_to_data_by_sense(
                df['contextual_info'].values, df['sense_id'].values, df['pos'].values)

            data = data.groupby(['sense_and_pos', 'sense', 'year', 'category'])[
                'counts'].sum().reset_index()

            mask = data.category.isin([selected_source])
            fig = px.line(data[mask], x='year',
                            y='counts', color='sense_and_pos', markers=True)

            fig.update_xaxes(
                categoryorder='category ascending', linecolor='gray', tickangle=-45)
            fig.update_yaxes(linecolor='gray',
                                gridcolor='#D3D3D3', gridwidth=0.5)
            fig.update_layout(
                legend_title_text='Word Sense',
                xaxis_title='Year',
                yaxis_title='Number of Appearances',
                plot_bgcolor='white'
            )

            return fig

        raise PreventUpdate
