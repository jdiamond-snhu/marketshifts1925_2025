import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Set up Streamlit page environment layout
st.set_page_config(page_title="Macro History Dashboard", layout="wide")

st.title("📈 100 Years of Macroeconomics (1925 - 2025)")
st.subheader("Dual-Axis tracking of Market Growth vs. Annual Inflation Rate")

# 1. Generate historical proxy data spanning 1925 to 2025
@st.cache_data
def load_historical_data():
    years = np.arange(1925, 2026)
    
    # Simulate S&P 500 growth trajectory starting from a base index of 100
    # Incorporates historical crashes (1929, 1970s, 2000, 2008) and secular bull runs
    market_values = []
    current_val = 100.0
    
    np.random.seed(42) # Seed to ensure consistency across re-runs
    for y in years:
        if y >= 1929 and y <= 1932:  # Great Depression crash
            growth = np.random.uniform(-0.25, -0.10)
        elif y == 2000 or y == 2001 or y == 2008: # Dot-com and GFC corrections
            growth = np.random.uniform(-0.20, -0.05)
        else:  # Standard compounding expansion years
            growth = np.random.uniform(0.05, 0.14)
            
        current_val *= (1 + growth)
        market_values.append(current_val)
        
    # Simulate US Inflation rate fluctuations 
    inflation_rates = []
    for y in years:
        if y >= 1930 and y <= 1933: # Great Depression deflation
            inf = np.random.uniform(-10.0, -2.0)
        elif y >= 1973 and y <= 1981: # 1970s Great Inflation stagflation
            inf = np.random.uniform(6.0, 13.5)
        elif y in [2021, 2022]: # Post-pandemic supply shock spikes
            inf = np.random.uniform(4.5, 8.0)
        else: # Standard modern targeted baseline stability
            inf = np.random.uniform(1.5, 3.5)
        inflation_rates.append(inf)

    df = pd.DataFrame({
        "Year": years,
        "Market_Value": market_values,
        "Inflation_Rate": inflation_rates
    })
    return df

df = load_historical_data()

# 2. Build the interactive Plotly Dual-Axis graph object
fig = go.Figure()

# Add Primary Trace: Market Value (Left Y-Axis)
fig.add_trace(go.Scatter(
    x=df["Year"],
    y=df["Market_Value"],
    name="Market Index Value (Left Axis)",
    mode="lines",
    line=dict(color="#1f77b4", width=3)
))

# Add Secondary Trace: Inflation Rate (Right Y-Axis)
fig.add_trace(go.Scatter(
    x=df["Year"],
    y=df["Inflation_Rate"],
    name="Inflation Rate % (Right Axis)",
    mode="lines",
    line=dict(color="#ff7f0e", width=2, dash="dash"),
    yaxis="y2" # Targets the secondary axis parameter
))

# 3. Design structural dual layout settings
fig.update_layout(
    xaxis=dict(title="Timeline (Years)", tickmode="linear", dtick=10),
    yaxis=dict(
        title="Total Market Index Base Value",
        titlefont=dict(color="#1f77b4"),
        tickfont=dict(color="#1f77b4"),
        type="log" # Logarithmic scale handles 100-year compound growth cleaner
    ),
    yaxis2=dict(
        title="Annual Inflation Rate (%)",
        titlefont=dict(color="#ff7f0e"),
        tickfont=dict(color="#ff7f0e"),
        anchor="x",
        overlaying="y",
        side="right",
        showgrid=False # Keeps background lines from overlapping confusingly
    ),
    legend=dict(x=0.01, y=0.99, borderwidth=1),
    hovermode="x unified",
    height=600
)

# 4. Render directly within the Streamlit frontend layout interface
st.plotly_chart(fig, use_container_width=True)

# 5. Display simple data summary tables underneath
st.markdown("### 🗒️ Data Overview Options")
show_data = st.checkbox("Toggle Raw Dataset Table")
if show_data:
    st.dataframe(df.style.format({"Market_Value": "{:,.2f}", "Inflation_Rate": "{:.2f}%"}), height=300)
