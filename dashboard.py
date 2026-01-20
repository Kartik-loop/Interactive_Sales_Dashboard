import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Executive Sales Dashboard", layout="wide")
st.title("📊 Interactive Sales Performance Dashboard")

# --- 2. DATA LOADING ---
@st.cache_data
def load_data():
    try:
        # Load data
        df = pd.read_csv('sales_data (2).csv')
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Simulate Profit (Same logic as notebook)
        np.random.seed(42)
        df['Profit_Margin'] = np.random.uniform(0.10, 0.30, size=len(df))
        df['Profit'] = df['Total_Sales'] * df['Profit_Margin']
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

# --- 3. SIDEBAR FILTERS ---
st.sidebar.header("Filter Options")

if not df.empty:
    # Product Filter
    selected_product = st.sidebar.multiselect(
        "Select Product:",
        options=df["Product"].unique(),
        default=df["Product"].unique()
    )

    # Region Filter
    selected_region = st.sidebar.multiselect(
        "Select Region:",
        options=df["Region"].unique(),
        default=df["Region"].unique()
    )

    # Filter Data
    filtered_df = df[
        (df["Product"].isin(selected_product)) & 
        (df["Region"].isin(selected_region))
    ]

    # --- 4. KPI METRICS ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${filtered_df['Total_Sales'].sum():,.2f}")
    col2.metric("Est. Profit", f"${filtered_df['Profit'].sum():,.2f}")
    col3.metric("Transactions", len(filtered_df))

    st.markdown("---")

    # --- 5. CHARTS (ROW 1) ---
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("Sales Trend")
        daily_sales = filtered_df.sort_values('Date')
        fig_line = px.line(daily_sales, x='Date', y='Total_Sales', markers=True)
        st.plotly_chart(fig_line, use_container_width=True)
    
    with c2:
        st.subheader("Region Share")
        fig_pie = px.pie(filtered_df, names='Region', values='Total_Sales', hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- 6. CHARTS (ROW 2) ---
    c3, c4 = st.columns(2)
    
    with c3:
        st.subheader("Profit Analysis")
        fig_scat = px.scatter(filtered_df, x="Total_Sales", y="Profit", color="Region", size="Quantity")
        st.plotly_chart(fig_scat, use_container_width=True)
        
    with c4:
        st.subheader("Product Performance")
        fig_box = px.box(filtered_df, x="Product", y="Total_Sales", color="Product")
        st.plotly_chart(fig_box, use_container_width=True)
