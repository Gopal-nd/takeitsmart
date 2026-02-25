
import numpy as np
import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Generate Synthetic Sales Data
np.random.seed(42)
n = 500

data = pd.DataFrame({
    "Month": np.random.choice(
        ["Jan","Feb","Mar","Apr","May","Jun",
         "Jul","Aug","Sep","Oct","Nov","Dec"], n),
    "Region": np.random.choice(
        ["North","South","East","West"], n),
    "Category": np.random.choice(
        ["Electronics","Clothing","Furniture"], n),
    "Sales": np.random.randint(1000, 10000, n),
    "Profit": np.random.randint(200, 3000, n),
})

# Initialize Dash App
app = Dash(__name__)
app.title = "Sales Dashboard"

app.layout = html.Div([
    html.H1("📊 Sales Dashboard", style={"textAlign": "center"}),

    html.Label("Select Region:"),
    dcc.Dropdown(
        id="region-dropdown",
        options=[{"label": r, "value": r} for r in data["Region"].unique()],
        value="North"
    ),

    dcc.Graph(id="sales-line"),
    dcc.Graph(id="category-bar")
])

@app.callback(
    [Output("sales-line", "figure"),
     Output("category-bar", "figure")],
    [Input("region-dropdown", "value")]
)
def update_dashboard(selected_region):

    filtered = data[data["Region"] == selected_region]

    monthly = filtered.groupby("Month")["Sales"].sum().reset_index()
    category = filtered.groupby("Category")["Sales"].sum().reset_index()

    line_fig = px.line(monthly, x="Month", y="Sales",
                       title=f"Monthly Sales - {selected_region}")

    bar_fig = px.bar(category, x="Category", y="Sales",
                     title=f"Category Sales - {selected_region}")

    return line_fig, bar_fig

if __name__ == "__main__":
    app.run(debug=True)