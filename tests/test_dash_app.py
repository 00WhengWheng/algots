import dash
from dash import html, dcc

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Test Dash App'),
    dcc.Dropdown(
        id='test-dropdown',
        options=[{'label': i, 'value': i} for i in ['A', 'B', 'C']],
        value='A'
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)