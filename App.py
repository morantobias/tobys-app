#app is latest working
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from pandas_datareader import data as web
from datetime import datetime as dt
import plotly.graph_objs as go
#latest working

import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
from pandas_datareader import data as web
from datetime import datetime as dt
import plotly.graph_objs as go
import numpy as np


app = dash.Dash(_name_)
server = app.server

app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions']=True

app.layout = html.Div([


	html.Div([
		html.H4('Enter a stock symbol'),
                html.H5 ('for australian stocks use symbol + .AX eg WBC.AX'),
		dcc.Input(id='input-1-state',type='text',value='AAPL'),
		html.Button('Submit',id='submit-button')
	]),


	dcc.Tabs(
                tabs=[
                    {'label': 'Price', 'value': 1},
		    {'label': 'Returns', 'value': 2},
                    {'label': 'Volatility', 'value': 3}
               	],
		#detrmines default tab to show                 
		value=1,id='tabs'
     	),
   
	html.Div(id='tab-output')
    	 ], 	style={
		'width': '60%',
       	 	'fontFamily': 'Sans-Serif',
		'margin-left': 'auto',
		'margin-right': 'auto'}
)

@app.callback(Output('tab-output', 'children'), 
	     [Input('tabs', 'value')],
	     events=[Event('submit-button', 'click')],  
	     state=[State('input-1-state', 'value')])
def display_content(value,stock_ticker):
	
	df = web.DataReader(
        stock_ticker, data_source='yahoo',
        start=dt(2017, 1, 1), end=dt.now())

	x = df.index
	price = df.Close #need Adj Close.
	volume = df.Volume
	vol = price.pct_change()
        perc_ret = (np.exp(np.log1p(vol).cumsum())-1)*100


	if value==1:
#no seperate tab for return. have scale for return on right side of price graph.
#see wind streaming app to simply return of graph and trace attributes
#option for line & candlestick
#stock tickers example for search box - compile a csv file for all exchanges, or dynamic?
#graph multiple traces
#drag bar to change scale
#introduce commentary

		return html.Div([   
			dcc.Graph(
           	 	id='price',
            		figure={'data': [{
            			'x': x,
            			'y': price}],
				'layout': {'title': 'Price'
				}
        			}
			    ),
			dcc.Graph(
			id='volume',
			figure={'data': [go.Bar(x=x,y=volume)],
				'layout': {'title': 'Daily Volume'
				}
				}	
			    )
			])
	
	if value==2: 

		return html.Div([ 
			dcc.Graph(
           		 id='return',
            		figure={
				'data': [{
            				'x': x,
            				'y': perc_ret}],
			'layout': {'title': 'Cumulative Return'
				}
				}
			    ),
			])

	if value==3: 

		return html.Div([ 
			dcc.Graph(
           		 id='vol',
            		figure={'data': [{
            			'x': x,
            			'y': vol}]
        			}
			    ),
			
			dcc.Graph(
			id='volhist',
			figure={'data': [go.Histogram(
				x=df.Close.pct_change()
        			)]}
			    )
			])

	
if __name__ == '__main__':
    app.run_server(debug=True)
import numpy as np


app = dash.Dash()

app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions']=True

app.layout = html.Div([


	html.Div([
		html.H4('Enter a stock symbol'),
		dcc.Input(
		id='stock-submit',
   		placeholder='Enter a stock to analyse',
    		type='text',
    		value='AAPL',
		),
		html.Button('Submit', id='submit-stock')
		]),


	dcc.Tabs(
                tabs=[
                    {'label': 'Price', 'value': 1},
		    {'label': 'Returns', 'value': 2},
                    {'label': 'Volatility', 'value': 3}
               	],
		#detrmines default tab to show                 
		value=1,
                id='tabs'
           	 ),
   
	html.Div(id='tab-output')
    	 ], 	style={
		'width': '60%',
       	 	'fontFamily': 'Sans-Serif',
		'margin-left': 'auto',
		'margin-right': 'auto'
   	 })


@app.callback(Output('stock', 'value'),[Input('submit-stock', 'n_clicks')], state=[State('stock-submit', 'value')])
def update_stock(stock_submit_value):
	stock=stock_submit_value
   

@app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
def display_content(value):

	#error here as value passes is value of tab, eg 1 or 2 not value of input box	
	#temp fix change value to 'AAPL' need another call back
	
	
	df = web.DataReader(
        stock, data_source='yahoo',
        start=dt(2017, 1, 1), end=dt.now())

	x = df.index
	price = df.Close
	vol = df.Close.pct_change()
        perc_ret = (np.exp(np.log1p(vol).cumsum())-1)*100


	if value==1: 

		return html.Div([   
			dcc.Graph(
           	 	id='price',
            		figure={'data': [{
            			'x': x,
            			'y': price}]
        			}
			    )
			])
	#no seperate tab for return. have scale for return on right side of price graph.
	if value==2: 
	
		#trace1 = ... 
		#tracen = ...
		#plot traces in graph as per examples
		return html.Div([ 
			dcc.Graph(
           		 id='return',
            		figure={
				'data': [{
            				'x': x,
            				'y': perc_ret}]
				}
			    ),
			])

	if value==3: 

		return html.Div([ 
			dcc.Graph(
           		 id='vol',
            		figure={'data': [{
            			'x': x,
            			'y': vol}]
        			}
			    ),
			
			dcc.Graph(
			id='volhist',
			figure={'data': [go.Histogram(
				x=df.Close.pct_change()
        			)]}
			    )
			])

	
if __name__ == '__main__':
app.run_server(debug=True)
