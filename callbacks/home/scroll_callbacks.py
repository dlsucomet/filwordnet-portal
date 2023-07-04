from dash import Input, Output


def init_callback(app):
    app.clientside_callback(
        """
        function (n_clicks) {
            const sidebar_link = document.getElementById('senses-link');
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
        Input('senses-link', 'n_clicks'),
        prevent_initial_call=True
    )
