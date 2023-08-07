# Import libraries
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc



# Load the dataset
data = pd.read_csv('sales_data_sample.csv')
data.info()
# Create the Dash app
external_stylesheets = [dbc.themes.BOOTSTRAP]

app = Dash(__name__, external_stylesheets=external_stylesheets)


# Set up the app layout
dropdown1 = dcc.Dropdown(options=data['COUNTRY'].unique(),
                            value='USA',style= {"color":"#017D09","backgroundColor":"black",})
radioitem2 = dcc.RadioItems(options=data['YEAR_ID'].unique(),style={"color":"white",'text-align':'center'},
                            value=2003,labelStyle={'display':'inline-block', 'margin':'10px','font-size': '20px'})
radioitem1 = dcc.RadioItems(style={"color":"white",'text-align':'center'},
        id='metric-selector',
        options=[
            {'label': 'Order Count', 'value': 'QUANTITYORDERED'},
            {'label': 'Sales Revenue', 'value': 'SALES'}
        ],
        value='QUANTITYORDERED', labelStyle={'display':'inline-block', 'margin':'10px','font-size': '20px'}
    )


app.layout = html.Div([
    dbc.Row([html.H1('Vehicle sales Dashboard',style= {"color":"#017D09","backgroundColor":"black",}),html.H2("..",style= {"color":"black","backgroundColor":"black",})]
            ,style= {"backgroundColor":"black","border":"5px black solid"}),
    
    
    dbc.Row([radioitem1,
    dbc.Col([dcc.Graph(id='graph',style={"width":"100%",})],width=6),
    dbc.Col([dcc.Graph(id='graph1', style={"width": "100%",})],width=3),
    dbc.Col([dcc.Graph(id='graph2',style={"width":"100%",})],width=3),
    
    ]),
    html.Br(),
    dbc.Row([
    dbc.Col([dcc.Graph(id='graph3',style={"width":"100%",})],width=6),
    dbc.Col([dropdown1,dcc.Graph(id='graph4',style={"width": "100%",})],width=6,),
    
    
    ],),
    html.Br(),
    dbc.Row([radioitem2,
    dbc.Col([dcc.Graph(id='graph5',style={"width":"100%"})],width=4),
    dbc.Col([dcc.Graph(id='graph6', style={"width": "100%"})],width=4),
    dbc.Col([html.H2(id ="text1",style={"color":"white",'text-align':'center'}),html.H2(id ="text2",style={"color":"white",'text-align':'center'}),html.H2(id ="text3",style={"color":"white",'text-align':'center'})],width=4),
    ])
],style= {'backgroundColor':'black','border': '50px solid black',})

# Set up the callback function

@app.callback(
    Output(component_id='graph', component_property='figure'),
    Input('metric-selector', 'value')
)
def update_graph(metric):
    df_bar = data.groupby(['PRODUCTLINE'], as_index=False).agg({'QUANTITYORDERED':'count', 'SALES':'sum'})
    df_bar = df_bar.sort_values(by=metric, ascending=False)
    fig = px.bar(df_bar, x='PRODUCTLINE', y=metric, 
                 title=f"{metric} by YEAR_ID")
    fig.update_layout(paper_bgcolor = "black",
                      plot_bgcolor = "black",
                  title = {'x':0.5}, 
                  font = {"family" : "courier"})
    

    return fig

@app.callback(
    Output(component_id='graph1', component_property='figure'),
    Input('metric-selector', 'value')
)
def update_graph1(metric):
    df_line = data.groupby(['QTR_ID'], as_index=False).agg({'QUANTITYORDERED':'count', 'SALES':'sum',"YEAR_ID": 'count'} )
    df_line = df_line.sort_values(by=metric, ascending=False)
    fig = px.line(df_line, x='QTR_ID', y=metric, color='YEAR_ID',
                 title=f"{metric} by YEAR_ID")
    fig.update_layout(paper_bgcolor = "black",
                      plot_bgcolor = "black",
                  title = {'x':0.5}, 
                  font = {"family" : "courier"})
    

    return fig

@app.callback(
    Output(component_id='graph2', component_property='figure'),
    Input('metric-selector', 'value')
)
def update_graph2(metric):
    df_pie = data.groupby(['DEALSIZE'], as_index=False).agg({'QUANTITYORDERED':'count', 'SALES':'sum'})
    df_pie = df_pie.sort_values(by=metric, ascending=False)
    fig = px.pie(df_pie,
                       names='DEALSIZE', values=metric,
                       title=f"{metric} by DEALSIZE",
                       )
    
    fig.update_layout(paper_bgcolor = "black",
                      plot_bgcolor = "black",
                  title = {'x':0.5}, 
                  font = {"family" : "courier"})
    return fig


@app.callback(
    Output(component_id='graph3', component_property='figure'),
    Input(component_id=radioitem1, component_property='value')
)
def update_graph3(selected_productline):
    
    monthly_revenue = data.groupby(['YEAR_ID','MONTH_ID'])['SALES'].sum().reset_index()
    fig = px.line(monthly_revenue,
                       x='MONTH_ID', y='SALES',
                       color='YEAR_ID',
                       title=f'Avocado Prices in {selected_productline}')
    
    fig.update_layout(paper_bgcolor = "black",
                      plot_bgcolor = "black",
                  title = {'x':0.5}, 
                  font = {"family" : "courier"})
    return fig

    


@app.callback(
    Output(component_id='graph4', component_property='figure'),
    Input(component_id=dropdown1, component_property='value')
)
def update_graph4(selected_productline):
    filtered1 = data[data['COUNTRY'] == selected_productline]
    sales_with_productline = filtered1.groupby(['PRODUCTLINE'])['SALES'].sum().reset_index()
    fig = px.bar(sales_with_productline,
                       x='PRODUCTLINE', y='SALES',
                       title=f'Avocado Prices in {selected_productline}')
    
    fig.update_layout(paper_bgcolor = "black",
                      plot_bgcolor = "black",
                  title = {'x':0.5}, 
                  font = {"family" : "courier"})
    return fig


    

@app.callback(
    Output(component_id='graph5', component_property='figure'),
    Input(component_id=radioitem2, component_property='value')
)
def update_graph5(selected_productline):
    filtered1 = data[data['YEAR_ID'] == selected_productline]
    sales_with_productline = filtered1.groupby(['DEALSIZE'])['ORDERNUMBER'].count().reset_index()
    fig = px.pie(sales_with_productline,
                       names='DEALSIZE', values='ORDERNUMBER',hole = 0.4,
                       title=f'Avocado Prices in {selected_productline}')
    fig.update_layout(paper_bgcolor = "black",
                      plot_bgcolor = "black",
                  title = {'x':0.5}, 
                  font = {"family" : "courier"})
    return fig

    

@app.callback(
    Output(component_id='graph6', component_property='figure'),
    Input(component_id=radioitem2, component_property='value')
)
def update_graph6(selected_productline):
    filtered1 = data[data['YEAR_ID'] == selected_productline]
    sales_with_productline = filtered1.groupby(['STATUS'])['ORDERNUMBER'].count().reset_index()
    fig = px.pie(sales_with_productline,
                       names='STATUS', values='ORDERNUMBER',hole = 0.4,
                       title=f'Avocado Prices in {selected_productline}')
    fig.update_layout(paper_bgcolor = "black",
                      plot_bgcolor = "black",
                  title = {'x':0.5}, 
                  font = {"family" : "courier"})
    return fig

    

@app.callback(
    Output(component_id='text1', component_property='children'),
    Input(component_id=radioitem2, component_property='value')
)
def update_text(select_year):
    sales = data.groupby(['YEAR_ID'])['SALES'].sum().reset_index()
    current_year = sales[sales['YEAR_ID'] == select_year]['SALES'].sum()

    return current_year

@app.callback(
    Output(component_id='text2', component_property='children'),
    Input(component_id=radioitem2, component_property='value')
)
def update_text2(select_year):
    sales6 = data.groupby(['YEAR_ID'])['SALES'].sum().reset_index()
    sales6['PY'] = sales6['SALES'].shift(1)
    previous_year = sales6[sales6['YEAR_ID'] == select_year]['PY'].sum()

    return previous_year

@app.callback(
    Output(component_id='text3', component_property='children'),
    Input(component_id=radioitem2, component_property='value')
)
def update_text3(select_year):
    sales6 = data.groupby(['YEAR_ID'])['SALES'].sum().reset_index()
    sales6['PY'] = sales6['SALES'].shift(1)
    sales6['YOY Growth'] = sales6['SALES'].pct_change()
    sales6['YOY Growth'] = sales6['YOY Growth'] * 100
    previous_year_growth = sales6[sales6['YEAR_ID'] == select_year]['YOY Growth'].sum()

    return previous_year_growth

# Run local server
if __name__ == '__main__':
    app.run_server(debug=True)