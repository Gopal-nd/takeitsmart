import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("/home/gopal/takeitsmart/week7/pizza_sales/pizza_sales.csv")

# Data preprocessing
df['order_date'] = pd.to_datetime(df['order_date'], format='mixed')
df['month'] = df['order_date'].dt.strftime('%b')
df['day'] = df['order_date'].dt.day_name()

month_order = ['Jan','Feb','Mar','Apr','May','Jun',
               'Jul','Aug','Sep','Oct','Nov','Dec']

day_order = ['Monday','Tuesday','Wednesday','Thursday',
             'Friday','Saturday','Sunday']

app = dash.Dash(__name__)

app.layout = html.Div([

    html.H1("🍕 Pizza Sales Interactive Dashboard", style={'textAlign':'center'}),

    html.Br(),

    # KPI Section
    html.Div([
        html.Div(id='revenue'),
        html.Div(id='orders'),
        html.Div(id='pizzas'),
        html.Div(id='avg_order'),
        html.Div(id='avg_pizza')
    ], style={'display':'flex','justifyContent':'space-around','fontSize':'20px'}),

    html.Br(),

    # Trends
    html.Div([
        dcc.Graph(id='daily_chart'),
        dcc.Graph(id='monthly_chart')
    ], style={'display':'flex'}),

    # Breakdown
    html.Div([
        dcc.Graph(id='category_chart'),
        dcc.Graph(id='size_chart')
    ], style={'display':'flex'}),

    html.Br(),

    # Funnel
    dcc.Graph(id='funnel_chart'),

    html.H3("🏆 Top 5 Best Selling Pizzas"),

    html.Div([
        dcc.Graph(id='top_revenue'),
        dcc.Graph(id='top_quantity'),
        dcc.Graph(id='top_orders')
    ], style={'display':'flex'}),

    html.H3("💀 Bottom 5 Worst Selling Pizzas"),

    html.Div([
        dcc.Graph(id='worst_revenue'),
        dcc.Graph(id='worst_quantity'),
        dcc.Graph(id='worst_orders')
    ], style={'display':'flex'})

])


@app.callback(
[
    Output('revenue','children'),
    Output('orders','children'),
    Output('pizzas','children'),
    Output('avg_order','children'),
    Output('avg_pizza','children'),

    Output('daily_chart','figure'),
    Output('monthly_chart','figure'),

    Output('category_chart','figure'),
    Output('size_chart','figure'),

    Output('funnel_chart','figure'),

    Output('top_revenue','figure'),
    Output('top_quantity','figure'),
    Output('top_orders','figure'),

    Output('worst_revenue','figure'),
    Output('worst_quantity','figure'),
    Output('worst_orders','figure')
],
[
    Input('daily_chart','clickData'),
    Input('monthly_chart','clickData'),
    Input('category_chart','clickData'),
    Input('size_chart','clickData')
]
)
def update_dashboard(day_click, month_click, category_click, size_click):

    filtered_df = df.copy()

    # Day filter
    if day_click:
        day = day_click['points'][0]['x']
        filtered_df = filtered_df[filtered_df['day'] == day]

    # Month filter
    if month_click:
        month = month_click['points'][0]['x']
        filtered_df = filtered_df[filtered_df['month'] == month]

    # Category filter
    if category_click:
        category = category_click['points'][0]['label']
        filtered_df = filtered_df[filtered_df['pizza_category'] == category]

    # Size filter
    if size_click:
        size = size_click['points'][0]['label']
        filtered_df = filtered_df[filtered_df['pizza_size'] == size]

    # ================= KPI =================
    revenue = filtered_df['total_price'].sum()
    orders = filtered_df['order_id'].nunique()
    pizzas = filtered_df['quantity'].sum()
    avg_order = revenue / orders if orders else 0
    avg_pizza = pizzas / orders if orders else 0

    revenue_card = f"💰 Revenue: ${revenue:,.2f}"
    orders_card = f"📦 Orders: {orders}"
    pizzas_card = f"🍕 Pizzas Sold: {pizzas}"
    avg_card = f"📊 Avg Order Value: ${avg_order:.2f}"
    avg_pizza_card = f"🍕 Avg Pizzas/Order: {avg_pizza:.2f}"

    # ================= Charts =================

    # Daily Trend
    daily = filtered_df.groupby('day')['order_id'].nunique().reindex(day_order).reset_index()
    fig_daily = px.bar(daily, x='day', y='order_id', title="Daily Orders")

    # Monthly Trend
    monthly = filtered_df.groupby('month')['order_id'].nunique().reset_index()
    monthly['month'] = pd.Categorical(monthly['month'], categories=month_order, ordered=True)
    monthly = monthly.sort_values('month')
    fig_month = px.line(monthly, x='month', y='order_id', markers=True, title="Monthly Orders")

    # Category Pie
    category_sales = filtered_df.groupby('pizza_category')['total_price'].sum().reset_index()
    fig_category = px.pie(category_sales, names='pizza_category', values='total_price', title="Sales by Category")

    # Size Pie
    size_sales = filtered_df.groupby('pizza_size')['total_price'].sum().reset_index()
    fig_size = px.pie(size_sales, names='pizza_size', values='total_price', title="Sales by Size")

    # Funnel Chart
    funnel = filtered_df.groupby('pizza_category')['quantity'].sum().reset_index()
    fig_funnel = px.funnel(funnel, x='quantity', y='pizza_category', title="Total Pizzas Sold by Category")

    # Pizza Performance
    pizza_perf = filtered_df.groupby('pizza_name').agg({
        'total_price':'sum',
        'quantity':'sum',
        'order_id':'nunique'
    }).reset_index()

    # Top 5
    top_rev = pizza_perf.sort_values('total_price', ascending=False).head(5)
    top_qty = pizza_perf.sort_values('quantity', ascending=False).head(5)
    top_ord = pizza_perf.sort_values('order_id', ascending=False).head(5)

    fig_top_rev = px.bar(top_rev, x='total_price', y='pizza_name', orientation='h', title="Top Revenue")
    fig_top_qty = px.bar(top_qty, x='quantity', y='pizza_name', orientation='h', title="Top Quantity")
    fig_top_ord = px.bar(top_ord, x='order_id', y='pizza_name', orientation='h', title="Top Orders")

    # Bottom 5
    worst_rev = pizza_perf.sort_values('total_price').head(5)
    worst_qty = pizza_perf.sort_values('quantity').head(5)
    worst_ord = pizza_perf.sort_values('order_id').head(5)

    fig_worst_rev = px.bar(worst_rev, x='total_price', y='pizza_name', orientation='h', title="Worst Revenue")
    fig_worst_qty = px.bar(worst_qty, x='quantity', y='pizza_name', orientation='h', title="Worst Quantity")
    fig_worst_ord = px.bar(worst_ord, x='order_id', y='pizza_name', orientation='h', title="Worst Orders")

    return (
        revenue_card, orders_card, pizzas_card, avg_card, avg_pizza_card,
        fig_daily, fig_month,
        fig_category, fig_size,
        fig_funnel,
        fig_top_rev, fig_top_qty, fig_top_ord,
        fig_worst_rev, fig_worst_qty, fig_worst_ord
    )


if __name__ == '__main__':
    app.run(debug=True)