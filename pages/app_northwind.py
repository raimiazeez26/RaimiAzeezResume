import dash
from dash import Dash, html, dcc, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import base64
import plotly.graph_objects as go
import plotly.express as px
from .side_bar import sidebar

dash.register_page(__name__, order=6, name='Northwind Dashboard')

# ------------------------------------------------------------------------------
# FUNCTIONS TO CALCULATE KPIS
# ------------------------------------------------------------------------------

def revenue(df):
    rev = df['SalesAmount(USD)'].sum()
    return round(rev, 2)


def total_orders(df):
    orders = df['orderID'].unique()
    t_orders = len(orders)
    return int(t_orders)


def total_customers(df):
    cus = df['customerID'].unique()
    t_cus = len(cus)
    return t_cus


def total_employees(df):
    cus = df['employeeID'].unique()
    t_cus = len(cus)
    return t_cus


def avg_days_shipping(df):
    data = df[df['daysToShip'].notnull()]
    k = sum(data['daysToShip']) / len(data['daysToShip'])
    if k == float(np.NaN):
        return 0
    else:
        return round(float(k), 1)


def top_products(df):
    prods = df.groupby('productName').sum().reset_index().sort_values("SalesAmount(USD)", axis=0, ascending=False)

    top_prod = prods.head(5)
    fig = px.bar(top_prod, x="SalesAmount(USD)", y="productName", orientation='h',
                 )
    fig.update_traces(marker_color='#2e97a4')
    fig.update_coloraxes(showscale=False)
    fig.update_layout(
        title='Top Products',
        margin=dict(l=1, r=1, t=32, b=1),
    )
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    return fig


def top_productscat(df):
    categ = df.groupby('categoryName').sum().reset_index().sort_values("SalesAmount(USD)", axis=0, ascending=False)
    fig = go.Figure(go.Funnelarea(
        text=categ['categoryName'],
        values=categ['SalesAmount(USD)'],
        marker={"colors": ["teal", "#1a6985", "#2596be", "#25a5be", "#51abcb", "#92cbdf", "#bee0ec", "#bee0ec"]}
    ))

    fig.update_layout(
        title='Top Product Categories',
        margin=dict(l=1, r=1, t=32, b=1),
    )
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    fig.update(layout_showlegend=False)

    return fig


def top_productscatpx(df):
    prods = df.groupby('categoryName').sum().reset_index().sort_values("SalesAmount(USD)", axis=0, ascending=False)

    top_prod = prods.head(5)
    fig = px.pie(prods, names=prods['categoryName'], values=prods['SalesAmount(USD)'],
                 color=["#2e97a4", "#94c5d9", "#70a4a9", "#459fa8", "#94c1d4", "#8fbfdb", "#117466", "#c7cbcf"],
                 )
    fig.update_coloraxes(showscale=False)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        title='Top Product Categories',
        margin=dict(l=1, r=1, t=32, b=1),
    )
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig.update(layout_showlegend=False)
    return fig


def top_customers(df):
    cust = df.groupby('CustomertName').sum().reset_index().sort_values("SalesAmount(USD)", axis=0, ascending=False)

    top_cust = cust.head(5)
    fig = px.bar(top_cust, x="CustomertName", y="SalesAmount(USD)", hover_data=["SalesAmount(USD)"]
                 )
    fig.update_traces(marker_color='#2e97a4')
    fig.update_coloraxes(showscale=False)
    fig.update_layout(
        title='Top 5 Customers',
        margin=dict(l=1, r=1, t=32, b=1),
    )
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    return fig


def top_employees(df):
    dd = df.groupby(['employeeName', 'EmployeeCity', 'EmpReportsTo']).sum().reset_index()
    ds = dd[['employeeName', 'SalesAmount(USD)', 'EmployeeCity', 'EmpReportsTo']].sort_values("SalesAmount(USD)",
                                                                                              axis=0, ascending=False)
    ds = ds.rename(columns={'employeeName': 'Name', 'SalesAmount(USD)': 'Revenue', 'EmployeeCity': 'City',
                            'EmpReportsTo': 'Superior'})
    ds['Revenue'] = '$' + ds['Revenue'].astype(str)
    ds = ds.head(5)
    return ds


# sales revenue
def sales_revenue(df):
    dff = df.groupby(pd.to_datetime(df['orderDate']).dt.to_period('Q'))['SalesAmount(USD)'].sum()
    dff = pd.DataFrame(dff, columns=['SalesAmount(USD)'])
    dff['SumSales'] = dff['SalesAmount(USD)'].cumsum()
    dff.reset_index(inplace=True)
    dff['orderDate'] = dff['orderDate'].astype(str)

    fig = px.line(dff, x='orderDate', y='SumSales', title='Sales Revenue', markers='o')
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    fig.update_traces(line_color='#2e97a4')
    fig.update_coloraxes(showscale=False)
    fig.update_layout(
        margin=dict(l=1, r=1, t=30, b=1),
    )
    return fig


def order_shippers(df):
    data = df.groupby('companyNameShipper').sum().reset_index().sort_values("SalesAmount(USD)", axis=0, ascending=False)

    top_ship = data.head(5)
    fig = px.bar(top_ship, x="companyNameShipper", y="SalesAmount(USD)", hover_data=["SalesAmount(USD)"]
                 )
    fig.update_traces(marker_color='#2e97a4')
    fig.update_coloraxes(showscale=False)
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig.update_layout(
        title='Top Shippers',
        margin=dict(l=1, r=1, t=30, b=1),
    )

    return fig


def order_location(df):
    data = df.groupby('CustomerCountry').sum().reset_index()
    fig = px.scatter_geo(data, locationmode='country names', locations="CustomerCountry", color="CustomerCountry",
                         hover_name="CustomerCountry", size="SalesAmount(USD)", size_max=30,
                         projection="natural earth", color_discrete_sequence=px.colors.qualitative.Set3)

    fig.update_layout(autosize=True)
    fig.update_layout(title_text='Order Location', title_x=0.5)
    fig.update(layout_showlegend=False)
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
    )
    return fig


def freight(df):
    data = df.groupby('orderID').sum().reset_index()
    data['freight%'] = data['freight'] / data['SalesAmount(USD)']
    freight = np.sum(data['freight%'])

    return round(freight * 100, 2)


def oustanding_orders(df):
    outst = df['shippedDate'].isna().sum()
    return outst


data = pd.read_csv('assets/northwind.csv', index_col=[0])

# -------------------------------------------------------------------
# PRESET STYLES AND INDICATORS
# -------------------------------------------------------------------

indicator_style = {"height": '100%', 'border-radius': '13px',
                   'background': '#FFFFFF 0% 0% no-repeat padding-box',
                   'border': '1px solid  #CECECE',
                   'box-shadow': '3px 3px 6px #00000029', 'padding': '3px'}
# 'font-size': '16vmin'}

indicator_style_dark = {"height": '100%', 'border-radius': '13px',
                        'background': '##030000 0% 0% no-repeat padding-box',
                        'border': '1px solid  #CECECE',
                        'box-shadow': '3px 3px 6px #00000029', 'padding': '3px',
                        'font-size': '16vmin'}

graph_style = {"height": '100%', 'border-radius': '13px',
               'background': '#FFFFFF 0% 0% no-repeat padding-box',  ##FFFFFF
               'border': '1px solid  #CECECE',
               'box-shadow': '3px 3px 6px #00000029', 'padding': '3px',
               'font-size': '16vmin'}

col_style = {'background': '#FFFFFF 0% 0% no-repeat padding-box',
             'border-radius': '13px',
             'border': '1px solid  #CECECE', 'color': '#2e97a4',
             'box-shadow': '3px 3px 6px #00000029', 'padding': '3px'}

table_style = {"height": '100%', 'border-radius': '13px',
               'background': '#FFFFFF 0% 0% no-repeat padding-box',
               # 'border': '1px solid  #CECECE',
               # 'box-shadow': '3px 3px 6px #00000029', 'padding': '3px',
               'font-size': '1vmin', #'color': '#2e97a4'
               }


def indicator_curr(name, value, prev_val):
    fig = go.Figure(go.Indicator(mode="number+delta",
                                 title='<b>' + f'{name}' + '<b>',
                                 value=value,
                                 delta={'reference': prev_val, 'relative': True, "valueformat": ".2%"},
                                 number={'valueformat': '$,.0f'},
                                 domain={'x': [0, 1], 'y': [0, 1]}))
    fig.update_traces(number_font_size=18, title_font_size=12, title_font_family='Roboto',
                      title_font_color='#2e97a4', number_font_color='#2e97a4')  # "#211C51")

    return fig

def indicator(name, value, prev_val):
    fig = go.Figure(go.Indicator(mode="number+delta",
                                 title='<b>' + f'{name}' + '<b>',
                                 value=value,
                                 delta={'reference': prev_val, 'relative': True, "valueformat": ".2%"},
                                 # number={'valueformat': '$,.0f'},
                                 domain={'x': [0, 1], 'y': [0, 1]}))
    fig.update_traces(number_font_size=18, title_font_size=12, title_font_family='Roboto',
                      title_font_color='#2e97a4', number_font_color='#2e97a4')

    return fig


def indicator_days(name, value, prev_val):
    fig = go.Figure(go.Indicator(mode="number+delta",
                                 title='<b>' + f'{name}' + '<b>',
                                 value=value,
                                 delta={'reference': prev_val, 'relative': True, "valueformat": ".2%"},
                                 number={"suffix": " days"},
                                 domain={'x': [0, 1], 'y': [0, 1]}))
    fig.update_traces(number_font_size=18, title_font_size=12, title_font_family='Roboto',
                      title_font_color='#2e97a4', number_font_color='#2e97a4')

    return fig
# -------------------------------------------------------------------
# APPLICATION
# -------------------------------------------------------------------
#Year dropdown
timeframe_dropdown = html.Div([
    #html.P('Timeframe:'),
    dcc.Dropdown(
        id='year-dropdown',
        multi=False,
        #options=['2000', '2021', '2030'],
        options=[{'label': timeframe, 'value': timeframe} for timeframe in [2013, 2014, 2015]],
        value=None,
    )
], style={'width': '60%'})

def layout():
    return dbc.Container([
    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar()
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                    dbc.Container([
                        # Headers
                        dbc.Row([
                            # logo
                            dbc.Col([
                                html.Img(src='assets/northwind.jpg', className='text-center border',
                                         style={'width': '100%', 'height': '100%'}
                                         ),
                            ],  # width=2
                                xs=2, sm=2, md=2, lg=2, xl=2, style={"height": "100%"}, className='p-2', align='left'),

                            # heading title
                            dbc.Col([
                                html.H3('NORTHWIND TRADER ', className='text-center', style={"color": "#FFFFFF"}),
                                html.H5('Sales & Performance Dashboard', className='text-center',
                                        style={"color": "#FFFFFF"}),
                            ],  # width=6
                                xs=8, sm=8, md=8, lg=8, xl=8, className='p-1', align='center'),

                            # date filter
                            dbc.Col([
                                timeframe_dropdown
                            ],  # width=2,
                                xs=2, sm=2, md=2, lg=2, xl=2, style={'width': '10%', 'height': '100%'},
                                className='text-center p-2', align='right'),
                        ], justify='center', style={"height": "10%", 'background': '#2e97a4'}),
                        # , "background-color": "cyan"

                        # row1
                        dbc.Row([
                            dbc.Col([dcc.Graph(figure=indicator_curr('Total Revenue', revenue(data), None),
                                               style=indicator_style, config={'displayModeBar': False})],
                                    id='total-revenue', width=2, class_name='p-1 order-6'),
                            dbc.Col([dcc.Graph(figure=indicator('Orders', total_orders(data), None),
                                               style=indicator_style, config={'displayModeBar': False})],
                                    id='total-orders', width=2, class_name='p-1 '),
                            dbc.Col([dcc.Graph(figure=indicator_curr('Shipping Cost', freight(data), None),
                                               style=indicator_style, config={'displayModeBar': False})],
                                    id='total-shipping', width=2, class_name='p-1'),
                            dbc.Col([dcc.Graph(figure=indicator('No Of Customers', total_customers(data), None),
                                               style=indicator_style, config={'displayModeBar': False})],
                                    id='customers', width=2, class_name='p-1'),
                            dbc.Col([dcc.Graph(
                                figure=indicator_days('Shipping Delay', avg_days_shipping(data), None),
                                style=indicator_style, config={'displayModeBar': False})],
                                    id='shipping-days', width=2, class_name='p-1'),
                            dbc.Col([dcc.Graph(figure=indicator('Outstanding Orders', oustanding_orders(data), None),
                                               style=indicator_style, config={'displayModeBar': False})],
                                    id='outstanding-orders', width=2, class_name='p-1'),

                        ], justify='center', style={"height": "15%"}),

                        # row2
                        dbc.Row([

                            dbc.Col([dcc.Graph(figure=sales_revenue(data), style=graph_style,
                                               config={'displayModeBar': False})],
                                    width=6, class_name='p-1', id='sales-revenue'),
                            dbc.Col([dcc.Graph(figure=top_products(data), style=graph_style,
                                               config={'displayModeBar': False})],
                                    width=3, class_name='p-1', id='top-products'),
                            dbc.Col([dcc.Graph(figure=top_productscat(data), style=graph_style,
                                               config={'displayModeBar': False})],
                                    width=3, class_name='p-1', id='top-categories'),

                        ], justify='center', style={"height": "40%"}),

                        # row3
                        dbc.Row([

                            dbc.Col(
                                [dcc.Graph(figure=top_customers(data),
                                           style={"height": '100%', 'border-radius': '13px',
                                                  'background': '#FFFFFF 0% 0% no-repeat padding-box',  ##FFFFFF
                                                  },

                                           config={'displayModeBar': False})
                                 ], width=3, class_name='p-1', id='top-customers'),
                            dbc.Col([dcc.Graph(figure=order_location(data),
                                               style=graph_style,

                                               config={'displayModeBar': False})],
                                    width=3, class_name='p-1', id='order-location'),
                            dbc.Col([dcc.Graph(figure=order_shippers(data), style=graph_style,
                                               config={'displayModeBar': False})],
                                    width=3, class_name='p-1', id='top-shippers'),
                            dbc.Col([html.Div(children='Top Employees'),
                                     dbc.Table.from_dataframe(top_employees(data), striped=True, bordered=True,
                                                              hover=True, responsive=True, style=table_style,
                                                              id='top-employee-table', color="primary")
                                     ], width=3, class_name='p-1', style=col_style, id='top-employees'),

                        ], justify='center', style={"height": "35%"}),

                        # dcc.Store inside the user's current browser session
                        dcc.Store(id='store', data=[], storage_type='session'),  # 'local' or 'session' or 'memory'

                        # dcc.Store inside the user's current browser session previous year
                        dcc.Store(id='prev_store', data=[], storage_type='session')  # 'local' or 'session' or 'memory'

                    ], class_name='g-0 p-4',
                        style={"height": "99vh", 'background-image': 'url(/assets/northwind.jpg)',
                               'background-size': '100%'})  # fluid = True,

                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    )
], fluid=True, class_name='g-0 vh-100')

@callback(
    Output('store', 'data'),
    Output('prev_store', 'data'),
    Input('year-dropdown', 'value'),
    prevent_initial_call=True
)
def data_store(value):
    # hypothetical enormous dataset with millions of rows

    if value == None:
        data = pd.read_csv('assets/northwind.csv', index_col=[0])
        prev_data = pd.DataFrame()
        # print(f'data not selected {data}')
    else:
        data = pd.read_csv('assets/northwind.csv', index_col=[0])
        data = data[data.OrderYear.isin([value])]

        prev_data = pd.read_csv('assets/northwind.csv', index_col=[0])
        prev_data = prev_data[prev_data.OrderYear.isin([value - 1])]
        # print(f'data selected {data}')

    return data.to_dict('records'), prev_data.to_dict('records')


@callback(
    Output('total-revenue', 'children'),
    Output('total-orders', 'children'),
    Output('customers', 'children'),
    Output('outstanding-orders', 'children'),
    Output('total-shipping', 'children'),
    Output('shipping-days', 'children'),
    Input('store', 'data'),
    Input('prev_store', 'data'),
    prevent_initial_call=True
)
def update_indicators(data, prev_data):
    data = pd.DataFrame(data)
    prev_data = pd.DataFrame(prev_data)

    if len(prev_data) == 0:
        # revenue
        fig_rev = dcc.Graph(figure=indicator_curr('Total Revenue', revenue(data), None), style=indicator_style,
                            config={'displayModeBar': False})

        # orders
        fig_ord = dcc.Graph(figure=indicator('Total no Of Order', total_orders(data), None), style=indicator_style,
                            config={'displayModeBar': False})

        # shipping costs
        fig_ship = dcc.Graph(figure=indicator_curr('Total Cost of Shipping', freight(data), None),
                             style=indicator_style,
                             config={'displayModeBar': False})

        # customers
        fig_cust = dcc.Graph(figure=indicator('No Of Customers', total_customers(data), None), style=indicator_style,
                             config={'displayModeBar': False})

        # sales employees
        fig_outst = dcc.Graph(figure=indicator('Outstanding Orders', oustanding_orders(data), None),
                              style=indicator_style,
                              config={'displayModeBar': False})

        # shipping days
        fig_shippingdays = dcc.Graph(figure=indicator_days('Avg Days before Shipping', avg_days_shipping(data), None),
                                     style=indicator_style,
                                     config={'displayModeBar': False})

    else:
        # revenue
        fig_rev = dcc.Graph(figure=indicator_curr('Total Revenue', revenue(data), revenue(prev_data)),
                            style=indicator_style,
                            config={'displayModeBar': False})

        # orders
        fig_ord = dcc.Graph(figure=indicator('Total no Of Order', total_orders(data), total_orders(prev_data)),
                            style=indicator_style,
                            config={'displayModeBar': False})

        # shipping costs
        fig_ship = dcc.Graph(figure=indicator_curr('Total Cost of Shipping', freight(data), freight(prev_data)),
                             style=indicator_style,
                             config={'displayModeBar': False})

        # customers
        fig_cust = dcc.Graph(figure=indicator('No Of Customers', total_customers(data), total_customers(prev_data)),
                             style=indicator_style,
                             config={'displayModeBar': False})

        # Outstanding orders
        fig_outst = dcc.Graph(figure=indicator('Outstanding Orders', oustanding_orders(data), oustanding_orders(data)),
                              style=indicator_style,
                              config={'displayModeBar': False})

        # shipping days
        fig_shippingdays = dcc.Graph(
            figure=indicator_days('Avg Days before Shipping', avg_days_shipping(data), avg_days_shipping(prev_data)),
            style=indicator_style,
            config={'displayModeBar': False})

    return fig_rev, fig_ord, fig_ship, fig_cust, fig_outst, fig_shippingdays


@callback(
    Output('sales-revenue', 'children'),
    Output('top-products', 'children'),
    Output('top-categories', 'children'),
    Output('top-customers', 'children'),
    Output('order-location', 'children'),
    Output('top-shippers', 'children'),
    Output('top-employee-table', 'children'),
    Input('store', 'data'),
    prevent_initial_call=True
)
def update_graphs(data):
    data = pd.DataFrame(data)

    sales_rev = dcc.Graph(figure=sales_revenue(data), style=graph_style, config={'displayModeBar': False})
    top_prod = dcc.Graph(figure=top_products(data), style=graph_style, config={'displayModeBar': False})
    top_cat = dcc.Graph(figure=top_productscat(data), style=graph_style, config={'displayModeBar': False})
    top_cost = dcc.Graph(figure=top_customers(data), style=graph_style, config={'displayModeBar': False})
    ord_loc = dcc.Graph(figure=order_location(data), style=graph_style, config={'displayModeBar': False})
    top_ship = dcc.Graph(figure=order_shippers(data), style=graph_style, config={'displayModeBar': False})
    top_empl = dbc.Table.from_dataframe(top_employees(data), striped=True, bordered=True, hover=True, responsive=True,
                                        style=table_style, color="primary")

    return sales_rev, top_prod, top_cat, top_cost, ord_loc, top_ship, top_empl
