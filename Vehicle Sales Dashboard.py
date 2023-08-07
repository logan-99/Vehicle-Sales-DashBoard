# Import libraries
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc



# Load the dataset
data = pd.read_csv('sales_data_sample.csv')
#data.info()
data['QTR_ID'] = data['QTR_ID'].astype('category')
# Create the Dash app and linking relevent styles
external_stylesheets = [dbc.themes.BOOTSTRAP, 'style.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)


# Setting up the app layout
dropdown1 = dcc.Dropdown(options=data['COUNTRY'].unique(),
                         value='USA')
radioitem2 = dcc.RadioItems(
    options=data['YEAR_ID'].unique(),
    style={
        "color": "white",
        "text-align": "left",
        "margin-bottom": "15px"
    },
    value=2003,
    labelStyle={
        "display": "inline-block",
        "margin": "10px",
        "font-size": "20px"
    }
)

radioitem1 = dcc.RadioItems(
    style={
        "color": "white",
        "text-align": "center",
        "margin-bottom": "15px"
    },
    id="metric-selector",
    options=[        {"label": "Quantity Ordered", "value": "QUANTITYORDERED"},        {"label": "Sales Revenue", "value": "SALES"}    ],
    value="QUANTITYORDERED",
    labelStyle={
        "display": "inline-block",
        "margin": "10px",
        "font-size": "20px"
    }
)


app.layout = html.Div([
   dbc.Row([    html.H1('Vehicle sales Dashboard', style={"color": "#42F545", "background-color": "black",        "text-align": "center","font-size": "50px","font-weight": "bold", "font-family": "Lato"}), html.H2("..", style={        "color": "black","background-color": "black"    })], style={
    "background-color": "black",
    "border": "5px black solid"
}),
    
    dbc.Row([dbc.Col([html.H2("",style={"color": "white","font-size": "20px","align": "left"})],width=2),dbc.Col([radioitem2],width=4),dbc.Col([radioitem1],width=6),]),
    
    
    dbc.Row([
    dbc.Col([dcc.Graph(id='graph',style={"width":"100%","backgroundColor":"#202735",'border':'5px solid #202735','border-radius':'15px'})],width=5),
    dbc.Col([dcc.Graph(id='graph1', style={"width": "100%","backgroundColor":"#202735",'border':'5px solid #202735','border-radius':'15px'})],width=4),
    dbc.Col([dcc.Graph(id='graph2',style={"width":"100%","backgroundColor":"#202735",'border':'5px solid #202735','border-radius':'15px'})],width=3),
    
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([dcc.Graph(id='graph5',style={"width":"100%",'border':'5px solid #202735','border-radius':'15px'})],width=4),
        dbc.Col([dcc.Graph(id='graph6', style={"width": "100%",'border':'5px solid #202735','border-radius':'15px'})],width=4),
        dbc.Col([dbc.Row([html.H3("Current Year Total Sales Revenue",style={"color":"white",'text-align':'center','margin-top':'60px'})]),
                 dbc.Row([dbc.Col([html.H2( id ="text1",style={"color":"#42F545",'text-align':'center'})])]),
                 html.Br(),
                 html.Br(),
                 dbc.Row([html.H3("Previous Year Total Sales Revenue",style={"color":"white",'text-align':'center'})]),
                 dbc.Row([dbc.Col([html.H2( id ="text2",style={"color":"#42F545",'text-align':'center'})])]),
                 html.Br(),
                 html.Br(),
                 dbc.Row([html.H3("Year over Year Growth",style={"color":"white",'text-align':'center'})]),
                 dbc.Row([dbc.Col([html.H2( id ="text3",style={"color":"#42F545",'text-align':'center'})])]),]
                 
                 
                 ,style= {'backgroundColor':'#202735','border':'5px solid #202735','border-radius':'15px'},width=4),
    
    
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([dcc.Graph(id='graph3',style={"width":"100%",'border':'5px solid #202735','border-radius':'15px'})],width=6),
        dbc.Col([dropdown1,dcc.Graph(id='graph4',style={"width": "100%",'border':'5px solid #202735','border-radius':'15px'})],width=6,),
    
    ])
],style= {'backgroundColor':'black',"border":"25px black solid"} )

# Setting up the app callback function

@app.callback(
    Output(component_id='graph', component_property='figure'),
     
    [Input('metric-selector', 'value'),
     Input(component_id=radioitem2, component_property='value')]
)
def update_graph(metric,selected_year):
    
    filtered = data[data['YEAR_ID'] == selected_year]
    df_bar = filtered.groupby(['PRODUCTLINE'], as_index=False).agg({'QUANTITYORDERED':'count', 'SALES':'sum'})
    df_bar = df_bar.sort_values(by=metric, ascending=False)
    fig = px.bar(df_bar, x='PRODUCTLINE', y=metric, 
                 title=f"{metric} by PRODUCTLINE in {selected_year}",color="PRODUCTLINE", color_continuous_scale='Inferno')
    fig.update_traces(showlegend=False)
    fig.update_layout(
        paper_bgcolor="#202735",
        plot_bgcolor="#202735",
        title={'x': 0.5,
               'font': {'size': 22}},
        xaxis={
           'title': {
               'text': 'Productline',
               'font': {'size': 18}
           }
       },
       yaxis={
           'title': {
               'text': f'{metric}',
               'font': {'size': 18}}
       },
        font={"family": "courier", "color": "#42F545"},
        
    )
    
    return fig

@app.callback(
    Output(component_id='graph1', component_property='figure'),
    [Input('metric-selector', 'value'),
     Input(component_id=radioitem2, component_property='value')]
)
def update_graph1(metric,selected_year):
    filtered = data[data['YEAR_ID'] == selected_year]
    df_bar = filtered.groupby(['QTR_ID'], as_index=False).agg({'QUANTITYORDERED':'count', 'SALES':'sum',"YEAR_ID": 'count'} )
    df_bar = df_bar.sort_values(by=metric, ascending=False)
    
    fig = px.bar(df_bar, x=metric, y='QTR_ID', orientation='h',
                 title=f"{metric} by QTR_ID\nin {selected_year}",color="QTR_ID",color_continuous_scale='Inferno')
    fig.update_traces(showlegend=False)
    fig.update_layout(
        paper_bgcolor="#202735",
        plot_bgcolor="#202735",
        title={'x': 0.5,
               'font': {'size': 18}},
        xaxis={
           'title': {
               'text': f'{metric}',
               'font': {'size': 18}
           }
       },
       yaxis={
           'title': {
               'text': 'QTR_ID',
               'font': {'size': 18}}
       },
        font={"family": "courier", "color": "#42F545"},
        
    )
    
    return fig

@app.callback(
    Output(component_id='graph2', component_property='figure'),
    [Input('metric-selector', 'value'),
     Input(component_id=radioitem2, component_property='value')]
)
def update_graph2(metric,selected_year):
    filtered = data[data['YEAR_ID'] == selected_year]
    df_pie = filtered.groupby(['DEALSIZE'], as_index=False).agg({'QUANTITYORDERED':'count', 'SALES':'sum'})
    df_pie = df_pie.sort_values(by=metric, ascending=False)
    fig = px.pie(df_pie,
                       names='DEALSIZE', values=metric,
                       title=f"{metric} by DEALSIZE in {selected_year}",
                       )
    
    fig.update_layout(
        paper_bgcolor="#202735",
        plot_bgcolor="#202735",
        title={'x': 0.5,
               'font': {'size': 15}},
        font={"family": "courier", "color": "#42F545"},
        
    )
    return fig


@app.callback(
    Output(component_id='graph3', component_property='figure'),
    Input(component_id=dropdown1, component_property='value')
)
def update_graph3(selected_year):
    
    monthly_revenue = data.groupby(['YEAR_ID','MONTH_ID'])['SALES'].sum().reset_index()
    fig = px.line(monthly_revenue,
                       x='MONTH_ID', y='SALES',
                       color='YEAR_ID',
                       title='Sales over the years')
    
    fig.update_layout(
        paper_bgcolor="#202735",
        plot_bgcolor="#202735",
        title={'x': 0.5,
               'font': {'size': 22}},
        xaxis={
           'title': {
               'text': 'Month',
               'font': {'size': 18}
           }
       },
       yaxis={
           'title': {
               'text': "Total Sales (Dollars)",
               'font': {'size': 18}}
       },
        font={"family": "courier", "color": "#42F545"},
        
    )
    return fig

    


@app.callback(
    Output(component_id='graph4', component_property='figure'),
    Input(component_id=dropdown1, component_property='value')
)
def update_graph4(selected_country):
    filtered1 = data[data['COUNTRY'] == selected_country]
    df_bar = filtered1.groupby(['PRODUCTLINE'])['SALES'].sum().reset_index()
    fig = px.bar(df_bar,
                       x='PRODUCTLINE', y='SALES',
                       title=f'Productline Sales in {selected_country}',color='PRODUCTLINE')
    fig.update_traces(showlegend=False)
    fig.update_layout(
        paper_bgcolor="#202735",
        plot_bgcolor="#202735",
        title={'x': 0.5,
               'font': {'size': 22}},
        xaxis={
           'title': {
               'text': 'Productline',
               'font': {'size': 18}
           }
       },
       yaxis={
           'title': {
               'text': 'Sales (Dollars)',
               'font': {'size': 18}}
       },
        font={"family": "courier", "color": "#42F545"},
        
    )
    return fig


    

@app.callback(
    Output(component_id='graph5', component_property='figure'),
    Input(component_id=radioitem2, component_property='value')
)
def update_graph5(selected_year):
    filtered = data[data['YEAR_ID'] == selected_year]
    df_pie = filtered.groupby(['DEALSIZE'])['ORDERNUMBER'].count().reset_index()
    fig = px.pie(df_pie,
                       names='DEALSIZE', values='ORDERNUMBER',hole = 0.4,
                       title=f'DealSize spread in {selected_year}')
    fig.update_layout(
        paper_bgcolor="#202735",
        plot_bgcolor="#202735",
        title={'x': 0.5,
               'font': {'size': 22}},
        xaxis={
           'title': {
               'text': 'Productline',
               'font': {'size': 18}
           }
       },
       yaxis={
           'title': {
               'text': 'Sales',
               'font': {'size': 18}}
       },
        font={"family": "courier", "color": "#42F545"},
        
    )
    return fig

    

@app.callback(
    Output(component_id='graph6', component_property='figure'),
    Input(component_id=radioitem2, component_property='value')
)
def update_graph6(selected_year):
    filtered = data[data['YEAR_ID'] == selected_year]
    df_pie = filtered.groupby(['STATUS'])['ORDERNUMBER'].count().reset_index()
    fig = px.pie(df_pie,
                       names='STATUS', values='ORDERNUMBER',hole = 0.4,
                       title=f'Order Status Variation in {selected_year}')
    fig.update_layout(
        paper_bgcolor="#202735",
        plot_bgcolor="#202735",
        title={'x': 0.5,
               'font': {'size': 22}},
        xaxis={
           'title': {
               'text': 'Productline',
               'font': {'size': 18}
           }
       },
       yaxis={
           'title': {
               'text': 'Sales',
               'font': {'size': 18}}
       },
        font={"family": "courier", "color": "#42F545"},
        
    )
    return fig

    

@app.callback(
    Output(component_id='text1', component_property='children'),
    Input(component_id=radioitem2, component_property='value')
)
def update_text(select_year):
    sales = data.groupby(['YEAR_ID'])['SALES'].sum().reset_index()
    current_year = sales[sales['YEAR_ID'] == select_year]['SALES'].sum()
    if current_year != 0:
        return "${:,.2f}".format(current_year)
    else:
        return "N/A"

@app.callback(
    Output(component_id='text2', component_property='children'),
    Input(component_id=radioitem2, component_property='value')
)
def update_text2(select_year):
    sales6 = data.groupby(['YEAR_ID'])['SALES'].sum().reset_index()
    sales6['PY'] = sales6['SALES'].shift(1)
    previous_year = sales6[sales6['YEAR_ID'] == select_year]['PY'].sum()
    if previous_year != 0:
        return "${:,.2f}".format(previous_year)
    else:
        return "N/A"

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
    previous_year_growth_round = round(previous_year_growth)
    
    
    if previous_year_growth == 0:
        return "N/A"
    
    return str(previous_year_growth_round) + "%"


# Run local server
if __name__ == '__main__':
    app.run_server(debug=True)
    
    
#To view the dashboard.
#1. Run the code and wait kernal gives the browser link mostly (http://127.0.0.1:8050/)
#2. Copy and paste it on the browser


#----------------End of the code-------------#
#-------ST3011 - Statistical Programming
#------------------Group 06
#--s14822 - J.D.M.P Jayasinghe
#--s14942 - A.H.D Pigera
#--s15035 - W.A.S Dilshan
#--s15071 - A.M.A.I.A Premasiri
