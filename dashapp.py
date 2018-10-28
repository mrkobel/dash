import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

### LEARNING RESOURCES
# https://plot.ly/python/
# https://dash.plot.ly/
# http://pandas.pydata.org/pandas-docs/stable/
# Good interactive tutorial for pandas: https://www.datacamp.com/community/tutorials/pandas-tutorial-dataframe-python


###  GLOBAL VARIABLES
app = dash.Dash(__name__, external_stylesheets=['resources/style.css'])

#dataframe variable for data
dfCmp = pd.DataFrame() #compliance history
dfCrt = pd.DataFrame() #circuits history

### funtion definitions
# this function to import all data required for the dashboard & cleanup
def importData():
    global dfCmp
    global dfCrt

    dfCmp = pd.read_csv('data/standardization_history.csv')
    dfCrt = pd.read_csv('data/circuits_history.csv')
    #optional data cleanup
    # ...

# prepare compliance chart
def createChartCompliance():
    global dfCrt

    data = []

    # prepare&include first line trace with averages values
    traceAverges = go.Scatter(
        x=list(dfCmp.groupby('Timestamp').groups),
        y=dfCmp.groupby('Timestamp')['Hardware'].mean().tolist(),
        name='Averages',
        marker=go.scatter.Marker(symbol="square", size=15)
    )
    data.append(traceAverges)

    # prepare and include traces for all sites
    for s in list(dfCmp.groupby('Site Code').groups):
        d = go.Bar(
            x=dfCmp[dfCmp['Site Code'] == s]['Timestamp'],
            y=dfCmp[dfCmp['Site Code'] == s]['Hardware'],
            name=s
        )
        data.append(d)

    # define chart layout
    layout = go.Layout(
        yaxis=go.layout.YAxis(
            title="% compliance",
            range=[0.8, 1]
        )
    )

    return go.Figure(data=data, layout=layout)
    #   plotly.offline.plot(fig)

# creates chart for financial analysis
def createChartCircuits():
    global dfCrt

    data = []


    dfCrtGrpInternetTime = dfCrt[dfCrt['C_type'] == 'Internet'].groupby(['Timestamp'])
    dfCrtGrpMplsTime = dfCrt[dfCrt['C_type'] == 'MPLS'].groupby(['Timestamp'])

    # prepare&include first trace count of internet circuits
    traceCount = go.Scatter(
        x=list(dfCrtGrpInternetTime.groups),
        y=dfCrtGrpInternetTime['C_cost'].count().tolist(),
        name='Count of Internet',
        marker=go.scatter.Marker(symbol="square", size=15),
        yaxis='y2'
    )
    data.append(traceCount)

    # prepare&include first trace count of MPLS circuits
    traceCount = go.Scatter(
        x=list(dfCrtGrpMplsTime.groups),
        y=dfCrtGrpMplsTime['C_cost'].count().tolist(),
        name='Count of MPLS',
        marker=go.scatter.Marker(symbol="square", size=15),
        yaxis='y2'
    )
    data.append(traceCount)



    # prepare&include first trace with internet costs
    traceCostsInternet = go.Bar(
        x=list(dfCrtGrpInternetTime.groups),
        y=dfCrtGrpInternetTime['C_cost'].sum().tolist(),
        name='Internet costs',
    )
    data.append(traceCostsInternet)

    # prepare&include first trace with MPLS costs
    traceCostsInternet = go.Bar(
        x=list(dfCrtGrpMplsTime.groups),
        y=dfCrtGrpMplsTime['C_cost'].sum().tolist(),
        name='MPLS costs',
    )
    data.append(traceCostsInternet)

    # define chart layout
    layout = go.Layout(
        barmode='stack',
        yaxis=go.layout.YAxis(
            title="PLN",
            # range=[0.8, 1]
        ),
        yaxis2=dict(
            title='yaxis2 title',
            titlefont=dict(
                color='rgb(148, 103, 189)'
            ),
            tickfont=dict(
                color='rgb(148, 103, 189)'
            ),
            overlaying='y',
            side='right'
        )

    )

    return go.Figure(data=data, layout=layout)
    #   plotly.offline.plot(fig)


#generates Dashboard using previous functions
def generateDashboard():

    figCompliance = createChartCompliance()
    figCircuits = createChartCircuits()

    app.layout = html.Div(children=[
        html.H1(children='DSV network dashboard'),
        html.Div(children='This will blow your mind, Jens...'),
        dcc.Graph(
            id='example-graph-1',
            figure=figCompliance
        ),
        dcc.Graph(
            id='example-graph-2',
            figure=figCircuits
        )

    ])


if __name__ == '__main__':
    # import data into pandas dataframe
    importData()

    # generate dashboard
    generateDashboard()

    # run server
    app.run_server()