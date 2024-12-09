import sys
from pathlib import Path
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta

# Add the project root to the Python path
project_root = str(Path(__file__).resolve().parents[1])
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backtesting.backtest import Backtester
from data.data_fetcher import DataFetcher
from config.strategy_config import STRATEGY_REGISTRY

# Initialize components
backtester = Backtester()
data_fetcher = DataFetcher()

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout
app.layout = dbc.Container([
    html.H1('AlgoTS Dashboard'),

    dbc.Row([
        dbc.Col([
            html.H2('Strategy Backtesting'),
            dbc.Form([
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Select Strategy:'),
                        dcc.Dropdown(
                            id='strategy-selector',
                            options=[{'label': k, 'value': k} for k in STRATEGY_REGISTRY.keys()],
                            value=list(STRATEGY_REGISTRY.keys())[0]
                        )
                    ])
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Symbol:'),
                        dbc.Input(id='symbol-input', value='BTC/USD', type='text')
                    ])
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Time Period:'),
                        dcc.DatePickerRange(
                            id='date-range',
                            start_date=(datetime.now() - timedelta(days=365)).date(),
                            end_date=datetime.now().date()
                        )
                    ])
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Timeframe:'),
                        dcc.Dropdown(
                            id='timeframe-selector',
                            options=[
                                {'label': '1 minute', 'value': '1m'},
                                {'label': '5 minutes', 'value': '5m'},
                                {'label': '15 minutes', 'value': '15m'},
                                {'label': '1 hour', 'value': '1h'},
                                {'label': '4 hours', 'value': '4h'},
                                {'label': '1 day', 'value': '1d'}
                            ],
                            value='1h'
                        )
                    ])
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button('Run Backtest', id='run-backtest', color='primary')
                    ])
                ])
            ])
        ], md=4),
        dbc.Col([
            dcc.Graph(id='equity-curve'),
            html.Div(id='metrics-display'),
            html.Div(id='trades-table')
        ], md=8)
    ])
], fluid=True)

@app.callback(
    [Output('equity-curve', 'figure'),
     Output('metrics-display', 'children'),
     Output('trades-table', 'children')],
    [Input('run-backtest', 'n_clicks')],
    [State('strategy-selector', 'value'),
     State('symbol-input', 'value'),
     State('date-range', 'start_date'),
     State('date-range', 'end_date'),
     State('timeframe-selector', 'value')]
)
def run_backtest(n_clicks, strategy_name, symbol, start_date, end_date, timeframe):
    if n_clicks is None:
        return {}, [], []

    try:
        # Fetch data
        data = data_fetcher.fetch_data(symbol, start_date, end_date, timeframe)

        # Run backtest
        results = backtester.run(strategy_name, data)

        # Create equity curve
        equity_curve = go.Figure(data=[go.Scatter(x=results['equity'].index, y=results['equity'].values)])
        equity_curve.update_layout(title='Equity Curve', xaxis_title='Date', yaxis_title='Equity')

        # Create metrics display
        metrics = [
            html.H4("Backtest Metrics"),
            html.P(f"Total Return: {results['total_return']:.2f}%"),
            html.P(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}"),
            html.P(f"Max Drawdown: {results['max_drawdown']:.2f}%"),
            html.P(f"Win Rate: {results['win_rate']:.2f}%")
        ]

        # Create trades table
        trades_df = pd.DataFrame(results['trades'])
        trades_table = dbc.Table.from_dataframe(trades_df, striped=True, bordered=True, hover=True)

        return equity_curve, metrics, trades_table

    except Exception as e:
        return {}, html.Div(f"Error: {str(e)}", style={'color': 'red'}), []

if __name__ == '__main__':
    app.run_server(debug=True)