import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import os

try:
    WORKING_EXAMPLE = int(os.environ["WORKING_EXAMPLE"])
except KeyError:
    WORKING_EXAMPLE = 1

if WORKING_EXAMPLE:
    title = html.H3("The working example:")
else:
    title = html.H3("The not-working example:")

app = dash.Dash(__name__)

fig = go.Figure(go.Scatter(x=[1, 2, 3], y=[4, 1, 0]))
app.layout = html.Div(
    id="base",
    children=[
        title,
        html.Div(id="display1"),
        dcc.Graph(id="graph", figure=fig),
        html.Button("Click here", id="update-display"),
        html.P(
            "Everytime you click the button the number displayed "
            "and the last y value in the plot should increase. "
            "Note: you have to reset the page after restarting "
            "the server to get th most up-to-date JavaScript loaded "
            "into the browser."
        ),
    ],
)

if WORKING_EXAMPLE:
    # This correctly updates the figure
    app.clientside_callback(
        """
    function(update_display_n_clicks,figure_) {
        console.log("figure");
        console.log(figure_);
        let figure = JSON.parse(JSON.stringify(figure_));
        if (!update_display_n_clicks) {
            update_display_n_clicks = 0;
        }
        figure.data[0].y[2]=update_display_n_clicks;
        console.log("figure_");
        console.log(figure);
        return [update_display_n_clicks,figure];
    }
    """,
        [Output("display1", "children"), Output("graph", "figure")],
        [Input("update-display", "n_clicks")],
        [State("graph", "figure")],
    )
else:
    # This doesn't update the figure
    app.clientside_callback(
        """
    function(update_display_n_clicks,figure_) {
        console.log("figure");
        console.log(figure_);
        let figure = {...figure_};
        if (!update_display_n_clicks) {
            update_display_n_clicks = 0;
        }
        figure.data[0].y[2]=update_display_n_clicks;
        console.log("figure_");
        console.log(figure);
        return [update_display_n_clicks,figure];
    }
    """,
        [Output("display1", "children"), Output("graph", "figure")],
        [Input("update-display", "n_clicks")],
        [State("graph", "figure")],
    )

if __name__ == "__main__":
    app.run_server(debug=True)
