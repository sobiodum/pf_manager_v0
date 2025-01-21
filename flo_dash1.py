from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


df = pd.read_csv('/Users/floriankockler/Code/GitHub.nosync/pf_manager_v0/data/portfolio_USD_20240122_20250121.csv')

app = Dash(__name__, external_stylesheets=external_stylesheets)


colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
df_table = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app.layout = html.Div([
    html.H1(children='Portfolio Trader', style={'textAlign':'center'}),
    dcc.Dropdown(
        options=['AAPL US Equity', 'MSFT US Equity'],
        value='AAPL US Equity', 
        id='dropdown-selection'
    ),
    dcc.Graph(id='graph-content'),
    html.H4(children='US Agriculture Exports (2011)'),
    generate_table(df_table),
    html.Button(id='submit-button-state', n_clicks=0, children='Submit'),

])
@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    return px.line(df, x='date', y=value, title=f'{value} Equity')

   
if __name__ == '__main__':
    app.run(debug=True)
