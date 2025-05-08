# iowrt_dashboard.py

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# ---- 1️⃣ Load Dataset Directly from Parquet URL ----
URL_DATA = 'https://storage.dosm.gov.my/iowrt/iowrt.parquet'
df = pd.read_parquet(URL_DATA)

# Ensure 'date' is datetime
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])

# ---- 2️⃣ Preprocess Data ----
df = df.sort_values('date')
df = df.fillna(0)

# Optional: Moving average of key index (12-month)
if 'overall' in df.columns:
    df['overall_MA12'] = df['overall'].rolling(window=12).mean()

# ---- 3️⃣ Streamlit Dashboard Layout ----
st.title("🇲🇾 Malaysia Index of Wholesale & Retail Trade Dashboard")
st.write("Visualizing official IoWRT data from DOSM (Department of Statistics Malaysia)")

# Date range filter
date_range = st.slider("Select Year Range:",
                       min_value=df['date'].min().year,
                       max_value=df['date'].max().year,
                       value=(df['date'].min().year, df['date'].max().year))

filtered_df = df[(df['date'].dt.year >= date_range[0]) & (df['date'].dt.year <= date_range[1])]

# ---- Line Chart - Overall Index ----
if 'overall' in df.columns:
    st.subheader("Overall Wholesale & Retail Trade Index (Monthly)")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(filtered_df['date'], filtered_df['overall'], label='Actual Index', marker='o')
    ax.plot(filtered_df['date'], filtered_df['overall_MA12'], label='12-Month MA', linestyle='--')
    ax.set_xlabel("Date")
    ax.set_ylabel("Index Value")
    ax.legend()
    st.pyplot(fig)

# ---- Bar Chart - Sector Breakdown ----
sectors = ['wholesale', 'retail', 'motor_vehicles']
available_sectors = [col for col in sectors if col in df.columns]

if available_sectors:
    st.subheader("Trade Sector Index Breakdown")
    sector_df = filtered_df[['date'] + available_sectors].set_index('date')
    st.bar_chart(sector_df)

# ---- Summary Statistics ----
st.subheader("Summary Statistics")
st.write(filtered_df.describe())

# ---- Line Chart - Sales Trend Over Time ----
st.subheader("📈 Sales Trend Over Time (Monthly)")

fig2, ax2 = plt.subplots(figsize=(12, 5))
ax2.plot(filtered_df['date'], filtered_df['sales'], marker='o', color='tab:blue', label='Monthly Sales')
ax2.set_title('Monthly Sales Trend (IoWRT)', fontsize=14)
ax2.set_xlabel('Date')
ax2.set_ylabel('Sales Value')
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend()

st.pyplot(fig2)

# Calculate 3-month moving average
filtered_df['sales_MA3'] = filtered_df['sales'].rolling(window=3).mean()

fig3, ax3 = plt.subplots(figsize=(12, 5))
ax3.plot(filtered_df['date'], filtered_df['sales'], marker='o', alpha=0.6, label='Monthly Sales')
ax3.plot(filtered_df['date'], filtered_df['sales_MA3'], color='red', linewidth=2, label='3-Month Moving Average')
ax3.set_title('Monthly Sales Trend with 3-Month Moving Average', fontsize=14)
ax3.set_xlabel('Date')
ax3.set_ylabel('Sales Value')
ax3.grid(True, linestyle='--', alpha=0.5)
ax3.legend()

st.pyplot(fig3)

# ---- Optional: Raw Data ----
with st.expander("Show Raw Data"):
    st.dataframe(filtered_df)