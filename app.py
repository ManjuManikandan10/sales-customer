import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Page configuration for a professional look
st.set_page_config(
    page_title="Executive Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Premium" Design
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    [data-testid="stMetricValue"] {
        font-size: 28px;
        color: #1f77b4;
    }
    .stTitle {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        color: #262730;
    }
    </style>
    """, unsafe_allow_html=True)

# Data Loading
@st.cache_data
def load_data():
    file_path = "data/sales_data.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    return pd.DataFrame()

df = load_data()

if df.empty:
    st.error("Dataset not found. Please run the data generation script first.")
else:
    # --- SIDEBAR FILTERS ---
    st.sidebar.title("Dashboard Filters")
    
    # Date Range Filter
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
    
    # Multi-select filters
    regions = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
    categories = st.sidebar.multiselect("Select Category", options=df['Category'].unique(), default=df['Category'].unique())

    # Filtering data based on selection
    mask = (df['Region'].isin(regions)) & (df['Category'].isin(categories))
    if len(date_range) == 2:
        start_date, end_date = date_range
        mask = mask & (df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)
    
    filtered_df = df.loc[mask]

    # --- DASHBOARD HEADER ---
    st.title("🚀 Sales Performance Dashboard")
    st.markdown("Real-time analysis of sales, profit, and product trends.")

    # --- KPI METRICS ---
    col1, col2, col3, col4 = st.columns(4)
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    total_orders = filtered_df['Order ID'].nunique()
    avg_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0

    col1.metric("Total Sales", f"${total_sales:,.0f}")
    col2.metric("Total Profit", f"${total_profit:,.0f}")
    col3.metric("Total Orders", f"{total_orders:,}")
    col4.metric("Avg Margin", f"{avg_margin:.1f}%")

    st.markdown("---")

    # --- VISUALIZATIONS ---
    row1_col1, row1_col2 = st.columns(2)

    # 1. Sales by Region (Bar Chart)
    fig_region = px.bar(
        filtered_df.groupby('Region')['Sales'].sum().reset_index(),
        x='Region', y='Sales',
        title="Sales by Region",
        color='Region',
        color_discrete_sequence=px.colors.qualitative.Prism,
        template='plotly_white'
    )
    row1_col1.plotly_chart(fig_region, use_container_width=True)

    # 2. Sales by Category (Pie Chart)
    fig_cat = px.pie(
        filtered_df, values='Sales', names='Category',
        title="Sales by Category",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel,
        template='plotly_white'
    )
    row1_col2.plotly_chart(fig_cat, use_container_width=True)

    row2_col1, row2_col2 = st.columns(2)

    # 3. Monthly Sales Trend (Line Chart)
    temp_df = filtered_df.copy()
    temp_df['Month-Year'] = temp_df['Date'].dt.to_period('M').astype(str)
    monthly_trend = temp_df.groupby('Month-Year')['Sales'].sum().reset_index()
    
    fig_trend = px.line(
        monthly_trend, x='Month-Year', y='Sales',
        title="Monthly Sales Trend",
        line_shape='spline',
        markers=True,
        template='plotly_white'
    )
    fig_trend.update_traces(line_color='#1f77b4', line_width=3)
    row2_col1.plotly_chart(fig_trend, use_container_width=True)

    # 4. Top Products by Profit (Column Chart)
    top_products = filtered_df.groupby('Product')['Profit'].sum().nlargest(10).reset_index()
    fig_prod = px.bar(
        top_products, x='Product', y='Profit',
        title="Top 10 Products by Profit",
        color='Profit',
        color_continuous_scale='Blues',
        template='plotly_white'
    )
    row2_col2.plotly_chart(fig_prod, use_container_width=True)

    # --- DATA TABLE ---
    st.markdown("### Raw Transaction Data")
    st.dataframe(filtered_df.sort_values(by='Date', ascending=False).head(100), use_container_width=True)

    st.sidebar.info(f"Viewing {len(filtered_df)} out of {len(df)} records.")

# To run this dashboard, type the following in your terminal:
# streamlit run "d:/data analysis/Sales_Dashboard_Project/app.py"
# Open your browser at: http://localhost:8501
