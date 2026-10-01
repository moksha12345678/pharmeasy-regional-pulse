
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="PharmEasy Regional Pulse",
    layout="wide"
)

DB_FILE = "pharmeasy.db"


@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_FILE)

    orders = pd.read_sql_query(
        """
        SELECT
            order_id,
            order_date,
            region,
            category,
            product,
            quantity,
            sales_inr,
            profit_inr
        FROM orders_clean
        """,
        conn
    )

    conn.close()

    orders["month"] = orders["order_date"].str[:7]

    return orders


df = load_data()

flagged_regions = {
    "Bengaluru",
    "Guntur",
    "Hyderabad",
    "Karimnagar",
    "Tirupati",
    "Vijayawada",
    "Visakhapatnam",
    "Warangal"
}

st.title("PharmEasy Regional Pulse Dashboard")
st.caption("April-June 2026 regional sales and profit analysis")


regions = ["All Regions"] + sorted(df["region"].unique().tolist())

selected_region = st.selectbox(
    "Select Region",
    regions
)


if selected_region == "All Regions":
    filtered_df = df.copy()
else:
    filtered_df = df[df["region"] == selected_region].copy()


total_sales = filtered_df["sales_inr"].sum()
total_profit = filtered_df["profit_inr"].sum()
total_orders = filtered_df["order_id"].nunique()


# ---------------- OVERVIEW ----------------

st.subheader("Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Sales (INR)",
    f"₹{total_sales:,.2f}"
)

col2.metric(
    "Total Profit (INR)",
    f"₹{total_profit:,.2f}"
)

col3.metric(
    "Distinct Order Count",
    f"{total_orders:,}"
)


# ---------------- EXECUTIVE SUMMARY ----------------

st.subheader("Executive Summary")

summary = (
    f"The dashboard reports total sales of ₹{total_sales:,.2f}, "
    f"total profit of ₹{total_profit:,.2f}, and {total_orders:,} distinct orders. "
    "Regional sales showed material month-over-month movement across April-June 2026, "
    "with eight unique regions flagged above the 8% threshold. "
    "Guntur recorded a +122.19% sales change from April to May, followed by a "
    "-28.11% change from May to June, indicating that the movement should be reviewed "
    "rather than treated as a confirmed sustained trend. "
    "Use the category breakdown, regional comparison, and region filter below "
    "to inspect where the sales movement is concentrated."
)

st.write(summary)


# ---------------- TREND ----------------

st.subheader("Trend — How did monthly sales change?")

monthly_sales = (
    filtered_df
    .groupby(["month", "region"], as_index=False)["sales_inr"]
    .sum()
)

fig_line = px.line(
    monthly_sales,
    x="month",
    y="sales_inr",
    color="region",
    markers=True,
    title="How did sales change from April to June?"
)

fig_line.update_xaxes(
    title="Month",
    type="category"
)

fig_line.update_yaxes(
    title="Sales (INR)",
    rangemode="tozero"
)

fig_line.update_layout(
    legend_title="Region"
)

st.plotly_chart(
    fig_line,
    use_container_width=True
)


# ---------------- REGIONAL COMPARISON ----------------

st.subheader(
    "Regional Comparison — Which regions generated the most sales?"
)

region_sales = (
    filtered_df
    .groupby("region", as_index=False)["sales_inr"]
    .sum()
    .sort_values("sales_inr", ascending=False)
)

fig_bar = px.bar(
    region_sales,
    x="region",
    y="sales_inr",
    title="Which regions generated the most total sales?",
    labels={
        "region": "Region",
        "sales_inr": "Sales (INR)"
    }
)

fig_bar.update_yaxes(
    rangemode="tozero"
)

bar_colors = [
    "crimson" if region in flagged_regions else "steelblue"
    for region in region_sales["region"]
]

fig_bar.update_traces(
    marker_color=bar_colors
)

st.plotly_chart(
    fig_bar,
    use_container_width=True
)


# ---------------- CATEGORY BREAKDOWN ----------------

st.subheader(
    "Category Breakdown — Which categories drive sales?"
)

category_sales = (
    filtered_df
    .groupby("category", as_index=False)["sales_inr"]
    .sum()
    .sort_values("sales_inr", ascending=False)
)

fig_pie = px.pie(
    category_sales,
    names="category",
    values="sales_inr",
    hole=0.45,
    title="Which categories make up total sales?"
)

st.plotly_chart(
    fig_pie,
    use_container_width=True
)


# ---------------- DETAIL ----------------

st.subheader("Detail — Regional Monthly Sales")

detail_table = (
    filtered_df
    .groupby(["region", "month"], as_index=False)
    .agg(
        sales_inr=("sales_inr", "sum"),
        profit_inr=("profit_inr", "sum"),
        order_count=("order_id", "nunique")
    )
    .sort_values(["region", "month"])
)

detail_table["sales_inr"] = detail_table["sales_inr"].round(2)
detail_table["profit_inr"] = detail_table["profit_inr"].round(2)

st.dataframe(
    detail_table,
    use_container_width=True,
    hide_index=True
)


st.info(
    "The region selector connects the overview KPIs, category breakdown, "
    "charts, and detail table. Order count uses distinct order_id values."
)
