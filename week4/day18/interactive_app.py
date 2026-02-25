import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np

# ----------------------------
# Generate Synthetic Data
# ----------------------------
np.random.seed(42)

dates = pd.date_range("2023-01-01", "2023-12-31")
regions = ["North", "South", "East", "West"]
products = ["Laptop", "Phone", "Tablet", "Monitor"]

data = []
for date in dates:
    for region in regions:
        for product in products:
            sales = np.random.randint(50, 500)
            profit = sales * np.random.uniform(0.1, 0.3)
            data.append([date, region, product, sales, profit])

df = pd.DataFrame(data, columns=["Date", "Region", "Product", "Sales", "Profit"])

# ----------------------------
# Initialize App
# ----------------------------
app = dash.Dash(__name__)
app.title = "Interactive Dashboard"

# ----------------------------
# Layout
# ----------------------------
app.layout = html.Div([

    html.H1("📊 Clickable Interactive Dashboard", style={"textAlign": "center"}),

    html.Button("Reset Filters", id="reset_btn", n_clicks=0),

    html.Div([
        html.Div(id="kpi_sales"),
        html.Div(id="kpi_profit"),
        html.Div(id="kpi_avg"),
    ], style={"display": "flex", "justifyContent": "space-around"}),

    dcc.Graph(id="line_chart"),
    dcc.Graph(id="bar_chart"),
    dcc.Graph(id="pie_chart"),

])

# ----------------------------
# Callback for Cross Filtering
# ----------------------------
@app.callback(
    [
        Output("line_chart", "figure"),
        Output("bar_chart", "figure"),
        Output("pie_chart", "figure"),
        Output("kpi_sales", "children"),
        Output("kpi_profit", "children"),
        Output("kpi_avg", "children"),
    ],
    [
        Input("bar_chart", "clickData"),
        Input("pie_chart", "clickData"),
        Input("line_chart", "clickData"),
        Input("reset_btn", "n_clicks")
    ]
)
def update_dashboard(bar_click, pie_click, line_click, reset_clicks):

    filtered_df = df.copy()

    ctx = dash.callback_context

    if ctx.triggered:
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger_id == "bar_chart" and bar_click:
            product_clicked = bar_click["points"][0]["x"]
            filtered_df = filtered_df[filtered_df["Product"] == product_clicked]

        elif trigger_id == "pie_chart" and pie_click:
            region_clicked = pie_click["points"][0]["label"]
            filtered_df = filtered_df[filtered_df["Region"] == region_clicked]

        elif trigger_id == "line_chart" and line_click:
            date_clicked = line_click["points"][0]["x"]
            filtered_df = filtered_df[filtered_df["Date"] == date_clicked]

        elif trigger_id == "reset_btn":
            filtered_df = df.copy()

    # KPIs
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    avg_sales = filtered_df["Sales"].mean()

    # Line Chart
    line_fig = px.line(
        filtered_df.groupby("Date")["Sales"].sum().reset_index(),
        x="Date",
        y="Sales",
        title="Sales Trend"
    )

    # Bar Chart
    bar_fig = px.bar(
        filtered_df.groupby("Product")["Sales"].sum().reset_index(),
        x="Product",
        y="Sales",
        title="Sales by Product",
        color="Product"
    )

    # Pie Chart
    pie_fig = px.pie(
        filtered_df.groupby("Region")["Sales"].sum().reset_index(),
        names="Region",
        values="Sales",
        title="Sales by Region"
    )

    return (
        line_fig,
        bar_fig,
        pie_fig,
        html.H3(f"Total Sales: ${total_sales:,.0f}"),
        html.H3(f"Total Profit: ${total_profit:,.0f}"),
        html.H3(f"Average Sales: ${avg_sales:,.2f}")
    )


# ----------------------------
# Run App
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)