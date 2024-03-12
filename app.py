from dash import dash, dcc, html, Input, Output
import requests
import pandas as pd
import datetime
import os

API_KEY = os.getenv('API_KEY', 'test')
app = dash.Dash()

app.layout = html.Div([
    html.H1("Historical Stock Data"),
    html.Div([
        html.Label("Select Stock Symbol:"),
        dcc.Dropdown(
            id='stock-dropdown',
            options=[
                {'label': 'Apple (AAPL)', 'value': 'AAPL'},
                {'label': 'Meta (META)', 'value': 'META'},
                {'label': 'Nvidia (NVDA)', 'value': 'NVDA'},
                {'label': 'Oracle (ORCL)', 'value': 'ORCL'},
                {'label': 'Microsoft (MSFT)', 'value': 'MSFT'},
            ],
            value='AAPL'
        )
    ]),
    html.Div([
        html.Label("Time Range:"),
        dcc.Dropdown(
            id='time-dropdown',
            options=[
                {'label': '6 Months', 'value': '6m'},
                {'label': '1 Year', 'value': '1y'},
                {'label': '5 Years', 'value': '5y'}
            ],
            value='5y'
        )
    ]),
    dcc.Graph(id='stock-graph'),
    dcc.Graph(id='finanical-graph'),
])

def fetch_stock_data(symbol, time_range):
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['historical']:
            stock_df = pd.DataFrame(data['historical'])
            stock_df['date'] = pd.to_datetime(stock_df['date'])

            if time_range == "1y":
                one_year_ago = datetime.datetime.now() - datetime.timedelta(days=365)
                mask = (stock_df['date'] > one_year_ago.strftime("%Y-%m-%d")) & (stock_df['date'] <= datetime.date.today().strftime("%Y-%m-%d"))
                stock_df = stock_df.loc[mask]
            elif time_range == "6m":
                one_year_ago = datetime.datetime.now() - datetime.timedelta(days=183)
                mask = (stock_df['date'] > one_year_ago.strftime("%Y-%m-%d")) & (stock_df['date'] <= datetime.date.today().strftime("%Y-%m-%d"))
                stock_df = stock_df.loc[mask]

            stock_df.set_index('date', inplace=True)
            return stock_df
    return None
def fetch_financial_data(symbol):
    url = f"https://financialmodelingprep.com/api/v3/financials/income-statement/{symbol}?apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['financials']:
            financials_df = pd.DataFrame(data['financials'])
            financials_df['date'] = pd.to_datetime(financials_df['date'])
            financials_df.set_index('date', inplace=True)
            return financials_df
    return None

@app.callback(
    [Output('stock-graph' , 'figure'),
    Output('finanical-graph' , 'figure')],
    [Input('stock-dropdown', 'value'),
    Input('time-dropdown', 'value')]
)
def update_graph(stock_symbol, time_range):
    figure1 = {}
    stock_data = fetch_stock_data(stock_symbol, time_range)
    if stock_data is not None:
        figure1={
            "data": [
                {
                    "x": stock_data.index,
                    "y": stock_data["close"],
                    "type": "line",
                    "name": stock_symbol
                },
            ],
            "layout": {
                "title": f"{stock_symbol} Historical Stock Price",
                "xaxis": {"title": "Date"},
                "yaxis": {"title": "Price (USD)"},
            },
        }
    else:
        figure1 = {'data': [], 'layout': {'title': f'No historical data found for {stock_symbol}'}}
    financial_data = fetch_financial_data(stock_symbol)
    figure2 = {}
    if financial_data is not None:
            figure2={
                "data": [
                    {"x": financial_data.index, "y": financial_data["Revenue"], "type": "bar", "name": "Revenue"},
                    {"x": financial_data.index, "y": financial_data["Net Income"], "type": "bar", "name": "Net Income"}
                ],
                "layout": {
                    "title": f"{stock_symbol} Income and Net Income Comparison",
                    "xaxis": {"title": "Date"},
                    "yaxis": {"title": "Amount (USD)"},
                },
            }
    else:
        figure2 = {'data': [], 'layout': {'title': f'No historical data found for {stock_symbol}'}}
    return [figure1, figure2]

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=8050)
