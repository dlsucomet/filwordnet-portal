from dash import Input, Output
import plotly.express as px


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
