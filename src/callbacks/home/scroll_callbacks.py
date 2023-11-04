from dash import Input, Output


def init_callback(app):
    app.clientside_callback(
        """
        function (n_clicks) {
            const yOffset = -1.2 * document.getElementById('search-word-div').clientHeight;
            const element = document.getElementById('network-row');
            const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;

            window.scrollTo({top: y, behavior: 'instant'});

            document.getElementById('senses-link').classList.remove('bold');
            document.getElementById('plot-sense-link').classList.remove('bold');
            document.getElementById('plot-source-link').classList.remove('bold');
            document.getElementById('embeddings-link').classList.remove('bold');
            document.getElementById('network-link').classList.add('bold');
            document.getElementById('export-link').classList.remove('bold');
        }
        """,
        Output('network-row', 'children'),
        Input('network-link', 'n_clicks'),
        prevent_initial_call=True
    )

    app.clientside_callback(
        """
        function (n_clicks) {
            const yOffset = -1.2 * document.getElementById('search-word-div').clientHeight; 
            const element = document.getElementById('plot-sense-row');
            const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;

            window.scrollTo({top: y, behavior: 'instant'});

            document.getElementById('senses-link').classList.remove('bold');
            document.getElementById('plot-sense-link').classList.add('bold');
            document.getElementById('plot-source-link').classList.remove('bold');
            document.getElementById('embeddings-link').classList.remove('bold');
            document.getElementById('network-link').classList.remove('bold');
            document.getElementById('export-link').classList.remove('bold');
        }
        """,
        Output('plot-sense-row', 'children'),
        Input('plot-sense-link', 'n_clicks'),
        prevent_initial_call=True
    )

    app.clientside_callback(
        """
        function (n_clicks) {
            const yOffset = -1.2 * document.getElementById('search-word-div').clientHeight; 
            const element = document.getElementById('plot-source-row');
            const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;

            window.scrollTo({top: y, behavior: 'instant'});

            document.getElementById('senses-link').classList.remove('bold');
            document.getElementById('plot-sense-link').classList.remove('bold');
            document.getElementById('plot-source-link').classList.add('bold');
            document.getElementById('embeddings-link').classList.remove('bold');
            document.getElementById('network-link').classList.remove('bold');
            document.getElementById('export-link').classList.remove('bold');
        }
        """,
        Output('plot-source-row', 'children'),
        Input('plot-source-link', 'n_clicks'),
        prevent_initial_call=True
    )

    app.clientside_callback(
        """
        function (n_clicks) {
            const yOffset = -1.2 * document.getElementById('search-word-div').clientHeight; 
            const element = document.getElementById('embeddings-row');
            const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;

            window.scrollTo({top: y, behavior: 'instant'});

            document.getElementById('senses-link').classList.remove('bold');
            document.getElementById('plot-sense-link').classList.remove('bold');
            document.getElementById('plot-source-link').classList.remove('bold');
            document.getElementById('embeddings-link').classList.add('bold');
            document.getElementById('network-link').classList.remove('bold');
            document.getElementById('export-link').classList.remove('bold');
        }
        """,
        Output('embeddings-row', 'children'),
        Input('embeddings-link', 'n_clicks'),
        prevent_initial_call=True
    )

    app.clientside_callback(
        """
        function (n_clicks) {                
            const yOffset = -1.2 * document.getElementById('search-word-div').clientHeight; 
            const element = document.getElementById('export-row');
            const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;

            window.scrollTo({top: y, behavior: 'instant'});

            document.getElementById('senses-link').classList.remove('bold');
            document.getElementById('plot-sense-link').classList.remove('bold');
            document.getElementById('plot-source-link').classList.remove('bold');
            document.getElementById('embeddings-link').classList.remove('bold');
            document.getElementById('network-link').classList.remove('bold');
            document.getElementById('export-link').classList.add('bold');
        }
        """,
        Output('export-row', 'children'),
        Input('export-link', 'n_clicks'),
        prevent_initial_call=True
    )

    app.clientside_callback(
        """
        function (n_clicks) {
            window.scrollTo({top: 0, behavior: 'instant'});

            document.getElementById('senses-link').classList.add('bold');
            document.getElementById('plot-sense-link').classList.remove('bold');
            document.getElementById('plot-source-link').classList.remove('bold');
            document.getElementById('embeddings-link').classList.remove('bold');
            document.getElementById('network-link').classList.remove('bold');
            document.getElementById('export-link').classList.remove('bold');
        }
        """,
        Output('senses-row', 'children'),
        Input('senses-link', 'n_clicks'),
        prevent_initial_call=True
    )
