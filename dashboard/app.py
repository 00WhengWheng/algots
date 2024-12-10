import sys
from pathlib import Path
import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash.long_callback import DiskcacheLongCallbackManager
import diskcache
import dash_bootstrap_components as dbc
from flask import Flask
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta

server = Flask(__name__)

import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta

# Add the project root to the Python path
project_root = str(Path(__file__).resolve().parents[1])
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backtesting.backtest import Backtester
from data.data_fetcher import DataFetcher
from strategies.strategy_loader import StrategyLoader
from config.strategy_config import STRATEGY_REGISTRY

# Initialize components
backtester = Backtester()
data_fetcher = DataFetcher()
strategy_loader = StrategyLoader()

# Initialize Dash app with long callback manager
cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], long_callback_manager=long_callback_manager)

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
                        dbc.Input(id='symbol-input', value='AAPL', type='text')
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

import asyncio

@app.long_callback(
    Output('equity-curve', 'figure'),
    Output('metrics-display', 'children'),
    Output('trades-table', 'children'),
    Input('run-backtest', 'n_clicks'),
    State('strategy-selector', 'value'),
    State('symbol-input', 'value'),
    State('date-range', 'start_date'),
    State('date-range', 'end_date'),
    State('timeframe-selector', 'value'),
    running=[
        (Output("run-backtest", "disabled"), True, False),
    ],
    prevent_initial_call=True
)

def run_backtest(n_clicks, strategy_name, symbol, start_date, end_date, timeframe):
    if n_clicks is None:
        return {}, "", []

    try:
        # Ensure all parameters are of the correct type
        symbol = str(symbol)
        start_date = pd.to_datetime(start_date).strftime('%Y-%m-%d')
        end_date = pd.to_datetime(end_date).strftime('%Y-%m-%d')
        interval = '1d'  # or use timeframe if it's the correct format

        # Fetch data
        data = data_fetcher.fetch_data_sync(symbol, start_date, end_date, source='alpha_vantage', interval=interval)
        
        if data is None or data.empty:
            raise ValueError(f"Failed to fetch data for {symbol}")

        # Run backtest
        results = backtester.run(strategy_name, data)

        # Create equity curve
        equity_curve = go.Figure(data=[go.Scatter(x=results.index, y=results['equity_curve'], mode='lines')])
        equity_curve.update_layout(title='Equity Curve', xaxis_title='Date', yaxis_title='Equity')

        # Display metrics
        metrics = html.Div([
            html.H3('Backtest Metrics'),
            html.P(f"Total Return: {results['total_return']:.2f}%"),
            html.P(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}"),
            html.P(f"Max Drawdown: {results['max_drawdown']:.2f}%")
        ])

        # Display trades table
        trades = results['trades']
        trades_table = dbc.Table.from_dataframe(trades, striped=True, bordered=True, hover=True)

        return equity_curve, metrics, trades_table

    except Exception as e:
        print(f"Error in run_backtest: {str(e)}")
        return {}, html.Div(f"Error: {str(e)}", style={'color': 'red'}), []

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)