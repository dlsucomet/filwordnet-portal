from dash import Input, Output


def init_callback(app):
    # app.clientside_callback(
    #     """
    #     function (n_clicks) {
    #         const sidebar_link = document.getElementById('network-link');
    #         sidebar_link.onclick = function(e) {
    #             e.preventDefault();
    #             e.stopPropagation();

    #             const yOffset = -1.2 * document.getElementById('search-word-div').clientHeight;
    #             const element = document.getElementById('network-row');
    #             const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;

    #             window.scrollTo({top: y, behavior: 'smooth'});
    #         };
    #     }
    #     """,
    #     Output('network-row', 'children'),
    #     Input('network-link', 'n_clicks'),
    #     prevent_initial_call=True
    # )

    app.clientside_callback(
        """
        function (n_clicks) {
            const sidebar_link = document.getElementById('plot-sense-link');
            sidebar_link.onclick = function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const yOffset = -1.2 * document.getElementById('search-word-div').clientHeight; 
                const element = document.getElementById('plot-sense-row');
                const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;

                window.scrollTo({top: y, behavior: 'smooth'});
            };
        }
        """,
        Output('plot-sense-row', 'children'),
        Input('plot-sense-link', 'n_clicks'),
        prevent_initial_call=True
    )

    app.clientside_callback(
        """
        function (n_clicks) {
            const sidebar_link = document.getElementById('plot-source-link');
            sidebar_link.onclick = function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const yOffset = -1.2 * document.getElementById('search-word-div').clientHeight; 
                const element = document.getElementById('plot-source-row');
                const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;

                window.scrollTo({top: y, behavior: 'smooth'});
            };
        }
        """,
        Output('plot-source-row', 'children'),
        Input('plot-source-link', 'n_clicks'),
        prevent_initial_call=True
    )

    app.clientside_callback(
        """
        function (n_clicks) {
            const sidebar_link = document.getElementById('embeddings-link');
            sidebar_link.onclick = function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const yOffset = -1.2 * document.getElementById('search-word-div').clientHeight; 
                const element = document.getElementById('embeddings-row');
                const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;

                window.scrollTo({top: y, behavior: 'smooth'});
            };
        }
        """,
        Output('embeddings-row', 'children'),
        Input('embeddings-link', 'n_clicks'),
        prevent_initial_call=True
    )

    app.clientside_callback(
        """
        function (n_clicks) {
            const sidebar_link = document.getElementById('export-link');
            sidebar_link.onclick = function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const yOffset = -1.2 * document.getElementById('search-word-div').clientHeight; 
                const element = document.getElementById('export-row');
                const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;

                window.scrollTo({top: y, behavior: 'smooth'});
            };
        }
        """,
        Output('export-row', 'children'),
        Input('export-link', 'n_clicks'),
        prevent_initial_call=True
    )
