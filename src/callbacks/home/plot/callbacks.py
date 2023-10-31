from dash import Input, Output, State, html
import dash_bootstrap_components as dbc

import plotly.express as px
from plotly.graph_objs import *
from dash.exceptions import PreventUpdate
from ..api_query import *
from .util import *
from ..sense.util import *


def init_callback(app, API_URL):
    @app.callback(
        Output('word-plot-sense', 'children'),
        Input('submitted-word', 'data'),
        Input('word-exists', 'data')
    )
    def display_word_in_the_sense_plot_description(word, word_exists):
        if word and word_exists:
            return [
                f' {word} ',
                html.I(className='bi bi-info-circle'),
                f' '
            ]

        raise PreventUpdate

    @app.callback(
        Output('word-plot-source', 'children'),
        Input('submitted-word', 'data'),
        Input('word-exists', 'data')
    )
    def display_word_in_the_source_plot_description(word, word_exists):
        if word and word_exists:        
            return [
                f' {word} ',
                html.I(className='bi bi-info-circle'),
                f' '
            ]

        raise PreventUpdate
    
    @app.callback(
        Output('word-plot-modal', 'children'),
        Output('word-plot-modal', 'is_open'),
        Input('word-plot-source', 'n_clicks'),
        Input('word-plot-sense', 'n_clicks'),
        State('submitted-word', 'data')
    )
    def display_word_tooltip_in_the_source_plot(source_n_clicks, sense_n_clicks, word):
        if source_n_clicks > 0 or sense_n_clicks > 0:
            df = get_word_db(API_URL, word)

            if len(df) >= 1:
                sense_list = []
                for i in range(len(df)):
                    sample_sentence_list = df.iloc[i]['example_sentences']

                    html_sample_sentence = html.Ul()
                    if len(sample_sentence_list) >= 1:
                        html_sample_sentence = html.Ul(
                            children=[
                                html.Li([
                                    html.Span('Sample sentence: '),
                                    html.Span(
                                        sample_sentence_list[0],
                                        style={'color': 'gray'}
                                    )
                                ])
                            ]
                        )

                    sense_list.append(
                        html.Li([
                            html.B(f'Sense {i+1}:'),
                            html_sample_sentence,
                            html.Br()
                        ]
                        )   
                    )


            modal = [
                dbc.ModalHeader(
                    dbc.ModalTitle(word)
                ),
                dbc.ModalBody([
                    html.Ul([
                        html.Li([
                            s for s in sense_list
                        ])
                    ])
                ])
            ]

            return modal, True
        
        raise PreventUpdate

    @app.callback(
        Output('sense-dropdown', 'options'),
        Output('sense-dropdown', 'value'),
        Input('submitted-word', 'data'),
        Input('word-exists', 'data')
    )
    def display_sense_dropdown(word, word_exists):
        if word and word_exists:
            df = get_word_db(API_URL, word)
            nlp_word_df = get_nlp_word(API_URL, word)

            checklist_options = {}
            num_sense = 0

            # netsci word 
            if len(df) >= 1:
                for i in range(len(df)):
                    sense_id = df.iloc[i]['sense_id']

                    pos = ''
                    #if 'pos' in df.columns:
                    #    pos = df.iloc[i]['pos']

                    checklist_options[sense_id] = sense_and_pos_text(
                        f'Sense {num_sense+1}', pos)
                    num_sense = num_sense + 1

            # nlp word
            if len(nlp_word_df) >= 1:
                for i in range(len(nlp_word_df)):
                    sense_id = nlp_word_df.iloc[i]['sense_id']

                    pos = ''
                    #if 'pos' in nlp_word_df.columns:
                    #    pos = nlp_word_df.iloc[i]['pos']

                    checklist_options[sense_id] = sense_and_pos_text(
                        f'Sense {num_sense+1}', pos) + "*"
                    num_sense = num_sense + 1


            if len(df) >= 1 or len(nlp_word_df) >= 1:
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
        Output('sense-sample-sentence', 'children'),
        Input('sense-dropdown', 'value'),
        Input('submitted-word', 'data'),
        Input('word-exists', 'data')
    )
    def plot_update_sample_sentence_base_on_sense(sense_value, word, word_exists):

        if word and sense_value and word_exists:
            df = get_word_db(API_URL, word)  # get_definition_list(word)
            
            if len(df) > 0:
                sense_id_df = df.loc[df['sense_id'] == sense_value.lower()]

                if len(sense_id_df) >= 1:
                    sample_sentence_list = sense_id_df.iloc[0]['example_sentences']

                    sample_sentence = ''
                    if len(sample_sentence_list) > 0:
                        sample_sentence = sample_sentence_list[0]

                    sense_data = html.Div(
                        children=[
                            html.Br(),
                            #html.Div(
                            #    children=[
                            #        html.Span('Definition: '),
                            #        html.Span(
                            #            'lorem ipsum',
                            #            style={'color': 'gray'}
                            #        )
                            #    ]
                            #),
                            html.Div(
                                children=[
                                    html.Span('Sample sentence: '),
                                    html.Span(
                                        sample_sentence,
                                        style={'color': 'gray'}
                                    )
                                ]
                            ),
                        ]
                    )
                    return sense_data

        raise PreventUpdate

    @app.callback(
        Output('graph-sense', 'figure'),
        Input('sense-dropdown', 'value'),
        Input('submitted-word', 'data'),
        Input('word-exists', 'data')
    )
    def update_line_chart(sense_value, word, word_exists):
        if word and word_exists:
            df = get_word_db(API_URL, word)

            pos = ''
            if 'pos' in df.columns:
                pos = df['pos'].values

            data = convert_to_data_by_sense(
                df['contextual_info'].values, df['sense_id'].values, pos)

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
        Input('submitted-word', 'data'),
        Input('word-exists', 'data')
    )
    def display_source_dropdown(word, word_exists):
        if word and word_exists:
            df = get_word_db(API_URL, word)
            
            if len(df) >= 1:

                pos = ''
                if 'pos' in df.columns:
                    pos = df['pos'].values

                data = convert_to_data_by_sense(
                    df['contextual_info'].values, df['sense_id'].values, pos)

                return data['category'].unique(), data['category'].unique()[0]
            else:
                # TODO: Handle case where word is not in database
                raise PreventUpdate

        raise PreventUpdate

    @app.callback(
        Output('graph-source', 'figure'),
        Input('source-dropdown', 'value'),
        Input('submitted-word', 'data'),
        Input('word-exists', 'data')
    )
    def update_line_chart(selected_source, word, word_exists):
        if word and word_exists:
            df = get_word_db(API_URL, word)
            pos = ''
            if 'pos' in df.columns:
                pos = df['pos'].values

            data = convert_to_data_by_sense(
                df['contextual_info'].values, df['sense_id'].values, pos)

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
