import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

###  GLOBAL VARIABLES
app = dash.Dash(__name__, external_stylesheets=['resources/style.css'])

#dataframe variable for data
df = pd.DataFrame()

### funtion definitions

# this function to import all data required for the dashboard
def importData():
    imported = pd.read_csv('data/standardization.csv')
    #optional data cleanup
    # ...
    return imported

#generates Dashboard
def generateDashboard():
    data = []

    #prepare&include first trace with averages values
    traceAverges = go.Scatter(
        x=list(df.groupby('Timestamp').groups),
        y=df.groupby('Timestamp')['Hardware'].mean().tolist(),
        name='Averages',
        marker=go.scatter.Marker(symbol="square", size=15)


    )
    data.append(traceAverges)

    #prepare and include traces for all sites
    for s in list(df.groupby('Site Code').groups):
        d = go.Bar(
                x=df[df['Site Code'] == s]['Timestamp'],
                y=df[df['Site Code'] == s]['Hardware'],
                name=s
            )
        data.append(d)

    #define chart layout
    layout = go.Layout(
        yaxis=go.layout.YAxis(
            title="% compliance",
            range=[0.8, 1]
        )
    )

    fig = go.Figure(data=data,layout=layout)

    app.layout = html.Div(children=[
        html.H1(children='DSV network dashboard'),
        html.Div(children='This will blow your mind, Jens...'),
        dcc.Graph(
            id='example-graph-2',
            figure=fig
        )
    ])


if __name__ == '__main__':
    # import data into pandas dataframe
    df = importData()

    # generate dashboard
    generateDashboard()

    # run server
    app.run_server()