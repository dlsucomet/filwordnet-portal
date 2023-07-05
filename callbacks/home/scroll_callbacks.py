from dash import Input, Output


def init_callback(app):
    app.clientside_callback(
        """
        function (n_clicks) {
            const sidebar_link = document.getElementById('network-link');
            sidebar_link.onclick = function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const yOffset = -1.2 * document.getElementById('search-word-div').clientHeight; 
                const element = document.getElementById('network-row');
                const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;

                window.scrollTo({top: y, behavior: 'smooth'});
            };
        }
        """,
        Output('network-row', 'children'),
        Input('network-link', 'n_clicks'),
        prevent_initial_call=True
    )
