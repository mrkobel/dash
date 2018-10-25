import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('sites.csv')


app.layout = html.Div([
    dcc.Graph(
        id='sites',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['WANServiceClassification'] == i]['SiteCode'],
                    y=df[df['WANServiceClassification'] == i]['White Collars Count'],
 #                   text=df[df['SiteCode'] == i]['SiteCode'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.WANServiceClassification.unique()
            ],
            'layout': go.Layout(
 #               xaxis={'type': 'log', 'title': 'GDP Per Capita'},
#                yaxis={'title': 'Life Expectancy'},
  #              margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
 #               legend={'x': 0, 'y': 1},
 #               hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server()