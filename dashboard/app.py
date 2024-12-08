import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objs as go
from datetime import datetime, timedelta
import pandas as pd
from config.strategy_config import STRATEGY_REGISTRY
from backtesting.backtest import Backtester
from data.data_fetcher import DataFetcher

app = dash.Dash(__name__)

# Initialize components
backtester = Backtester()
data_fetcher = DataFetcher()

app.layout = html.Div([
    html.H1('AlgoTS Dashboard'),
    
    # Backtesting Section
    html.Div([
        html.H2('Strategy Backtesting'),
        
        # Strategy Selection
        html.Div([
            html.Label('Select Strategy:'),
            dcc.Dropdown(
                id='strategy-selector',
                options=[{'label': k, 'value': k} for k in STRATEGY_REGISTRY.keys()],
                value=list(STRATEGY_REGISTRY.keys())[0]
            )
        ]),
        
        # Symbol Selection
        html.Div([
            html.Label('Symbol:'),
            dcc.Input(
                id='symbol-input',
                value='BTC/USD',
                type='text'
            )
        ]),
        
        # Time Period Selection
        html.Div([
            html.Label('Time Period:'),
            dcc.DatePickerRange(
                id='date-range',
                start_date=(datetime.now() - timedelta(days=365)).date(),
                end_date=datetime.now().date()
            ),
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
        ]),
        
        # Dynamic Strategy Parameters
        html.Div(id='strategy-parameters'),
        
        # Run Button
        html.Button('Run Backtest', id='run-backtest', n_clicks=0),
        
        # Results Section
        html.Div([
            # Equity Curve
            dcc.Graph(id='equity-curve'),
            
            # Metrics
            html.Div([
                html.Div(id='metrics-display', className='metrics-container'),
            ]),
            
            # Trade Table
            html.Div(id='trades-table')
        ], id='results-section')
    ])
])

@app.callback(
    Output('strategy-parameters', 'children'),
    Input('strategy-selector', 'value')
)
def update_strategy_parameters(strategy_name):
    if not strategy_name:
        return []
    
    params = STRATEGY_REGISTRY[strategy_name]['parameters']
    return [
        html.Div([
            html.Label(f"{param_name}:"),
            dcc.Input(
                id=f"param-{param_name}",
                type='number',
                value=param_config['default'],
                min=param_config.get('min'),
                max=param_config.get('max'),
                step=param_config.get('step', 1)
            )
        ]) for param_name, param_config in params.items()
    ]

@app.callback(
    [Output('equity-curve', 'figure'),
     Output('metrics-display', 'children'),
     Output('trades-table', 'children')],
    Input('run-backtest', 'n_clicks'),
    [State('strategy-selector', 'value'),
     State('symbol-input', 'value'),
     State('date-range', 'start_date'),
     State('date-range', 'end_date'),
     State('timeframe-selector', 'value')]
)
def run_backtest(n_clicks, strategy_name, symbol, start_date, end_date, timeframe):
    if n_clicks == 0:
        return {}, [], []
    
    # Fetch data
    data = data_fetcher.fetch_ohlcv(
        symbol=symbol,
        timeframe=timeframe,
        since=pd.Timestamp(start_date).timestamp() * 1000,
        until=pd.Timestamp(end_date).timestamp() * 1000
    )
    
    # Get strategy parameters
    strategy_params = {
        param_name: float(param_value)
        for param_name, param_value in [
            (p, dash.callback_context.inputs.get(f'param-{p}'))
            for p in STRATEGY_REGISTRY[strategy_name]['parameters'].keys()
        ]
    }
    
    # Run backtest
    results = backtester.run(strategy_name, data, strategy_params)
    
    # Create equity curve figure
    fig = go.Figure(data=[
        go.Scatter(
            x=results['equity_curve'].index,
            y=results['equity_curve'].values,
            mode='lines',
            name='Equity Curve'
        )
    ])
    
    # Create metrics display
    metrics = html.Div([
        html.H3('Performance Metrics'),
        html.P(f"Total Return: {results['total_return']:.2f}%"),
        html.P(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}"),
        html.P(f"Max Drawdown: {results['max_drawdown']:.2f}%"),
        html.P(f"Number of Trades: {results['trade_count']}")
    ])
    
    # Create trades table
    trades_table = html.Table(
        [html.Tr([html.Th(col) for col in results['trades'].columns])] +
        [html.Tr([html.Td(results['trades'].iloc[i][col]) for col in results['trades'].columns])
         for i in range(min(len(results['trades']), 10))]
    )
    
    return fig, metrics, trades_table

if __name__ == '__main__':
    app.run_server(debug=True)

# Add new section to the layout
html.Div([
    html.H2('Data Management'),
    
    # Data Collection Controls
    html.Div([
        html.Label('Symbol:'),
        dcc.Input(id='collect-symbol-input', value='BTC/USD', type='text'),
        
        html.Label('Source:'),
        dcc.Dropdown(
            id='data-source-selector',
            options=[
                {'label': 'Alpha Vantage', 'value': 'alpha_vantage'},
                {'label': 'Exchange', 'value': 'exchange'},
                {'label': 'Quandl', 'value': 'quandl'}
            ],
            value='exchange'
        ),
        
        html.Label('Timeframe:'),
        dcc.Dropdown(
            id='collect-timeframe-selector',
            options=[
                {'label': '1 minute', 'value': '1m'},
                {'label': '5 minutes', 'value': '5m'},
                {'label': '15 minutes', 'value': '15m'},
                {'label': '1 hour', 'value': '1h'},
                {'label': '4 hours', 'value': '4h'},
                {'label': '1 day', 'value': '1d'}
            ],
            value='1h'
        ),
        
        html.Button('Collect Data', id='collect-data-button', n_clicks=0),
    ]),
    
    # Data Preview
    html.Div([
        dcc.Graph(id='data-preview-chart'),
        html.Div(id='data-info')
    ])
]),

# Add callback for data collection
@app.callback(
    [Output('data-preview-chart', 'figure'),
     Output('data-info', 'children')],
    Input('collect-data-button', 'n_clicks'),
    [State('collect-symbol-input', 'value'),
     State('data-source-selector', 'value'),
     State('collect-timeframe-selector', 'value')]
)
def collect_and_preview_data(n_clicks, symbol, source, timeframe):
    if n_clicks == 0:
        return {}, []
    
    data_fetcher = DataFetcher()
    data = data_fetcher.update_dataset(symbol, source, timeframe)
    
    if data is None:
        return {}, html.Div('Error collecting data', style={'color': 'red'})
    
    # Create OHLCV chart
    fig = go.Figure(data=[
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close']
        )
    ])
    
    # Data information display
    info = html.Div([
        html.H4('Dataset Information'),
        html.P(f'Symbol: {symbol}'),
        html.P(f'Timeframe: {timeframe}'),
        html.P(f'Date Range: {data.index[0]} to {data.index[-1]}'),
        html.P(f'Number of Candles: {len(data)}')
    ])
    
    return fig, info
