import streamlit as st
import pandas as pd
import mysql.connector

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title("🛒 E-Commerce Sales Analysis Dashboard")
st.markdown("### Sales, Profit & Customer Analytics")

# =====================================================
# MYSQL CONNECTION
# =====================================================

connection = mysql.connector.connect(
    host=st.secrets["mysql"]["host"],
    user=st.secrets["mysql"]["user"],
    password=st.secrets["mysql"]["password"],
    database=st.secrets["mysql"]["database"]
)

# =====================================================
# LOAD DATA
# =====================================================

query = "SELECT * FROM cleaned_sales"

df = pd.read_sql(query, connection)

st.success("🟢 MySQL Connected Successfully!")

# =====================================================
# DATA PREPARATION
# =====================================================

df["Order Date"] = pd.to_datetime(df["Order Date"])

df["year"] = df["Order Date"].dt.year

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("🔎 Dashboard Filters")

# Available values
years = sorted(df["year"].dropna().unique())
categories = sorted(df["Category"].dropna().unique())
regions = sorted(df["Region"].dropna().unique())

# Date limits
min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()


# =====================================================
# RESET FUNCTION
# =====================================================

def reset_filters():

    st.session_state["year_filter"] = "All"
    st.session_state["category_filter"] = "All"
    st.session_state["region_filter"] = "All"
    st.session_state["date_filter"] = (min_date, max_date)


# =====================================================
# YEAR FILTER
# =====================================================

selected_year = st.sidebar.selectbox(
    "📅 Select Year",
    ["All"] + years,
    key="year_filter"
)


# =====================================================
# CATEGORY FILTER
# =====================================================

selected_category = st.sidebar.selectbox(
    "🏷️ Select Category",
    ["All"] + categories,
    key="category_filter"
)


# =====================================================
# REGION FILTER
# =====================================================

selected_region = st.sidebar.selectbox(
    "🌎 Select Region",
    ["All"] + regions,
    key="region_filter"
)


# =====================================================
# DATE FILTER
# =====================================================

selected_dates = st.sidebar.date_input(
    "📆 Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    key="date_filter"
)


# =====================================================
# RESET BUTTON
# =====================================================

st.sidebar.button(
    "🔄 Reset Filters",
    on_click=reset_filters
)

# =====================================================
# APPLY FILTERS
# =====================================================

filtered_df = df.copy()

if selected_year != "All":
    filtered_df = filtered_df[
        filtered_df["year"] == selected_year
    ]

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]


# Date Filter

if len(selected_dates) == 2:

    start_date, end_date = selected_dates

    filtered_df = filtered_df[
        (filtered_df["Order Date"].dt.date >= start_date)
        &
        (filtered_df["Order Date"].dt.date <= end_date)
    ]


# =====================================================
# KPI CALCULATIONS
# =====================================================

total_sales = filtered_df["Sales"].sum()

total_orders = filtered_df["Order ID"].nunique()

total_customers = filtered_df["Customer ID"].nunique()


# =====================================================
# KPI CARDS
# =====================================================

st.subheader("📊 Business Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Sales",
    f"${total_sales:,.2f}"
)


col2.metric(
    "📦 Total Orders",
    f"{total_orders:,}"
)

col3.metric(
    "👥 Total Customers",
    f"{total_customers:,}"
)

# =====================================================
# SALES BY CATEGORY & REGION
# =====================================================

category_sales = (
    filtered_df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

region_sales = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Sales by Category")
    st.bar_chart(category_sales)

with col2:
    st.subheader("🌎 Sales by Region")
    st.bar_chart(region_sales)

# =====================================================
# TOP 10 PRODUCTS
# =====================================================

st.subheader("🏆 Top 10 Products")

top_products = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_products)

# =====================================================
# MONTHLY SALES TREND
# =====================================================

monthly_sales = (
    filtered_df.groupby(
        filtered_df["Order Date"].dt.to_period("M")
    )["Sales"]
    .sum()
)

monthly_sales.index = monthly_sales.index.astype(str)

st.subheader("📅 Monthly Sales Trend")

st.line_chart(monthly_sales)

# =====================================================
# TOP 10 CUSTOMERS
# =====================================================

st.subheader("👥 Top 10 Customers")

top_customers = (
    filtered_df.groupby("Customer Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_customers)

# =====================================================
# SEGMENT & SHIP MODE ANALYSIS
# =====================================================

col1, col2 = st.columns(2)

with col1:

    segment_sales = (
        filtered_df.groupby("Segment")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.subheader("👥 Sales by Customer Segment")
    st.bar_chart(segment_sales)


with col2:

    ship_sales = (
        filtered_df.groupby("Ship Mode")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.subheader("🚚 Sales by Ship Mode")
    st.bar_chart(ship_sales)

# =====================================================
# TOP STATES & CITIES
# =====================================================

col1, col2 = st.columns(2)

with col1:

    state_sales = (
        filtered_df.groupby("State")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.subheader("📍 Top 10 States by Sales")
    st.bar_chart(state_sales)


with col2:

    city_sales = (
        filtered_df.groupby("City")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.subheader("🏙️ Top 10 Cities by Sales")
    st.bar_chart(city_sales)

# =====================================================
# ADDITIONAL SALES ANALYSIS
# =====================================================

st.subheader("📊 Additional Sales Analysis")


# State Analysis
if "state" in filtered_df.columns:

    state_sales = (
        filtered_df.groupby("State")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.write("### 📍 Top 10 States by Sales")
    st.bar_chart(state_sales)


# City Analysis
if "city" in filtered_df.columns:

    city_sales = (
        filtered_df.groupby("City")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.write("### 🏙️ Top 10 Cities by Sales")
    st.bar_chart(city_sales)


# =====================================================
# BUSINESS INSIGHTS
# =====================================================

st.subheader("💡 Key Business Insights")

best_category = (
    filtered_df.groupby("Category")["Sales"]
    .sum()
    .idxmax()
)

best_region = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
    .idxmax()
)

best_product = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .idxmax()
)

best_customer = (
    filtered_df.groupby("Customer Name")["Sales"]
    .sum()
    .idxmax()
)

col1, col2 = st.columns(2)

with col1:
    st.info(f"🏆 Highest Sales Category: **{best_category}**")
    st.info(f"🌎 Highest Sales Region: **{best_region}**")

with col2:
    st.info(f"📦 Top Product: **{best_product}**")
    st.info(f"👤 Top Customer: **{best_customer}**")

# =====================================================
# FILTERED DATA
# =====================================================

st.subheader("📋 Filtered Sales Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# =====================================================
# DOWNLOAD FILTERED DATA
# =====================================================

st.subheader("📥 Download Report")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇️ Download Filtered Sales Data",
    data=csv,
    file_name="e_commerce_filtered_sales.csv",
    mime="text/csv"
)