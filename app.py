import pandas as pd
import plotly.express as px

from dash import Dash, dcc, html, Input, Output

# Preparing your data for usage -----------------

# VVV Reading the file VVV
df = pd.read_csv("LA_PM2.5_25_data.csv")

# VVV Finding and sorting the data VVV
df["site_name"] = pd.Series(df["Local Site Name"]).str.lower()
df["date"] = pd.to_datetime(df["Date"])

# VVV Groups the data VVV
df = (
    df.groupby([df["date"].dt.date, "site_name"])[
        ["Daily AQI Value"]
    ]
    .mean()
    .astype(int)
)

df = df.reset_index()
print(df.head())

# App Layout ------------------------------------
stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(__name__, external_stylesheets=stylesheets)

app.layout = html.Div(
    [
        html.Div(
            html.H1("Hello", style={"textAlign": "center"}),
            className="row",
        ),
        html.Div(dcc.Graph(id="line-chart", figure={}), className="row"),
        html.Div(
            [
                html.Div(
                    dcc.Dropdown(
                        id = "my-dropdown",
                        multi = True,
                        options = [
                            {"label": x, "value": x}
                            for x in sorted(df["site_name"].unique())
                        ],
                        value = ["Compton","Pasadena"],
                    ),
                    className="two columns",
                ),
            ],
            className="row",
        ),
    ],
)


# Callbacks --------------------------------------
@app.callback(
    Output(component_id="line-chart", component_property="figure"),
    [Input(component_id="my-dropdown", component_property="value")],
)
def graph_update(Cvalue):
    if len(Cvalue) == 0:
        return {}
    else:
        df_filter = df[df["site_name"].isin(Cvalue)]
        fig = px.line(
            data_frame = df_filter,
            x = "date",
            y = "Daily AQI Value",
            color = "site_name",
            log_y = True,
            labels = {
                "Daily AQI Value": "AQI Values",
                "date":"Date",
                "site_name": "location",
            },
        )
        return fig

if __name__ == "__main__":
    app.run_server(debug=True)