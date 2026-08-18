import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(page_title="Macro History Dashboard", layout="wide")

st.title("📈 100 Years of Macroeconomics (1925 - 2025)")
st.subheader("Dual-Axis tracking of Market Growth vs. Annual Inflation Rate")
st.write("Jeff Diamond, 2026")
@st.cache_data
def load_historical_data():
    years = np.arange(1925, 2026)
    market_values = []
    current_val = 100.0
    
    np.random.seed(42)
    for y in years:
        if y >= 1929 and y <= 1932:
            growth = np.random.uniform(-0.25, -0.10)
        elif y in [2000, 2001, 2008]:
            growth = np.random.uniform(-0.20, -0.05)
        else:
            growth = np.random.uniform(0.05, 0.14)
            
        current_val *= (1 + growth)
        market_values.append(current_val)
        
    inflation_rates = []
    for y in years:
        if y >= 1930 and y <= 1933:
            inf = np.random.uniform(-10.0, -2.0)
        elif y >= 1973 and y <= 1981:
            inf = np.random.uniform(6.0, 13.5)
        elif y in [2021, 2022]:
            inf = np.random.uniform(4.5, 8.0)
        else:
            inf = np.random.uniform(1.5, 3.5)
        inflation_rates.append(inf)

    df = pd.DataFrame({
        "Year": years,
        "Market_Value": market_values,
        "Inflation_Rate": inflation_rates
    })
    return df

df = load_historical_data()

# --- NEW: MAP MACRO EVENTS TO SPECIFIC TIMELINES ---
# --- FULLY COMPREHENSIVE MACRO EVENTS LIST (1925 - 2025) ---
events = [
    {
        "start": 1929, "end": 1933, "color": "rgba(255, 0, 0, 0.05)", 
        "label": "Great Depression", "hover": "Great Depression: Stock crash & asset over-supply cuts markets by 80%+"
    },
    {
        "start": 1937, "end": 1938, "color": "rgba(142, 68, 173, 0.06)", 
        "label": "1937 Roosevelt Recession", "hover": "Recession of 1937: Premature fiscal tightening and monetary contracting forces a severe economic relapse"
    },
    {
        "start": 1945, "end": 1946, "color": "rgba(22, 160, 133, 0.06)", 
        "label": "Post-WWII Shock", "hover": "Post-War Demobilization: War spending stops causing a short structural drop, followed by a massive lifting of price controls"
    },
    {
        "start": 1951, "end": 1952, "color": "rgba(52, 152, 219, 0.07)", 
        "label": "1951 Fed-Treasury Accord", "hover": "Fed Autonomy Regained (1951): Historic Accord separates the Fed from Treasury control, allowing independent rate hikes to crush post-war inflation"
    },
    {
        "start": 1959, "end": 1960, "color": "rgba(39, 174, 96, 0.07)", 
        "label": "1959 Vault Cash Act", "hover": "Vault Cash Expansion (1959): Fed allows banks to count on-hand cash as legal reserves, instantly unlocking billions for suburban home loans"
    },
    {
        "start": 1971, "end": 1972, "color": "rgba(241, 196, 15, 0.07)", 
        "label": "Nixon Shock", "hover": "Nixon Shock (1971): US abandons the gold standard, destroying the Bretton Woods system & sparking fiat asset devaluation"
    },
    {
        "start": 1973, "end": 1981, "color": "rgba(255, 165, 0, 0.05)", 
        "label": "Great Inflation", "hover": "Stagflation Crisis: Oil supply shocks trigger runaway interest rates & market friction"
    },
    {
        "start": 1979, "end": 1980, "color": "rgba(0, 200, 200, 0.08)", 
        "label": "Silver Run & Crash", "hover": "Silver Corner Crash: Hunt brothers corner 1/3 of global silver, sparking a huge commodity spike & immediate collapse"
    },
    {
        "start": 1981, "end": 1985, "color": "rgba(41, 128, 185, 0.06)", 
        "label": "Volcker Rate Hikes", "hover": "Reagan-Volcker Solution: Fed raises interest rates to a record 20% to crush hyper-inflation, triggering a deliberate double-dip recession"
    },
    {
        "start": 1995, "end": 2001, "color": "rgba(46, 204, 113, 0.06)", 
        "label": "Dot-com Bubble", "hover": "Dot-com Crash: Extreme speculation in internet startups peaks in 2000, wiping out trillions in tech valuations"
    },
    {
        "start": 2007, "end": 2008, "color": "rgba(128, 0, 128, 0.05)", 
        "label": "Housing Crash", "hover": "Great Recession: Subprime mortgage defaults trigger a 20%+ banking market decline"
    },
    {
        "start": 2011, "end": 2012, "color": "rgba(0, 128, 0, 0.06)", 
        "label": "Euro Sovereign Debt", "hover": "Eurozone Crisis: High government debt in Greece/Italy triggers banking sector panic & bailouts"
    },
    {
        "start": 2013, "end": 2013, "color": "rgba(41, 128, 185, 0.06)", 
        "label": "Taper Tantrum", "hover": "Emerging Market Turmoil: Fed hints at scaling back QE, causing mass capital flight from developing markets"
    },
    {
        "start": 2014, "end": 2015, "color": "rgba(70, 130, 180, 0.06)", 
        "label": "Oil Price Collapse", "hover": "Crude Oil Crash: Massive oversupply from US shale and OPEC policy shift crashes oil prices by 50%+"
    },
    {
        "start": 2015, "end": 2016, "color": "rgba(220, 20, 60, 0.06)", 
        "label": "Puerto Rico Debt", "hover": "Puerto Rican Debt Crisis: Government defaults on $70B+ debt, prompting US federal restructuring intervention"
    },
    {
        "start": 2018, "end": 2019, "color": "rgba(255, 20, 147, 0.06)", 
        "label": "Crypto Winter", "hover": "Crypto Crash: Initial Coin Offering (ICO) bubble bursts, wiping out over 80% of total crypto market valuation"
    },
    {
        "start": 2020, "end": 2021, "color": "rgba(255, 0, 0, 0.06)", 
        "label": "COVID-19 Financial Shock", "hover": "COVID Financial Crisis: Global pandemic lockdowns spark sudden recession, saved by historic central bank stimulus"
    },
    {
        "start": 2022, "end": 2023, "color": "rgba(231, 76, 60, 0.06)", 
        "label": "2022 Fed Tightening", "hover": "Modern Rate Shock: Fed aggressively hikes interest rates from 0% to 5.25%+ to stomp out post-pandemic inflation, sparking a 19% bear market correction"
    }
]

# Map text descriptions to every single year in our main dataframe row index
df["Historical_Event"] = "Stable Market Cycle"  # Default text placeholder
for e in events:
    # If the year falls within the event boundaries, apply the custom text string
    df.loc[(df["Year"] >= e["start"]) & (df["Year"] <= e["end"]), "Historical_Event"] = e["hover"]

fig = go.Figure()

# Add Primary Trace: Market Value (Left Y-Axis)
fig.add_trace(go.Scatter(
    x=df["Year"], y=df["Market_Value"],
    name="Market Index Value", mode="lines",
    line=dict(color="#1f77b4", width=3)
))

# Add Secondary Trace: Inflation Rate (Right Y-Axis)
fig.add_trace(go.Scatter(
    x=df["Year"], y=df["Inflation_Rate"],
    name="Inflation Rate %", mode="lines",
    line=dict(color="#ff7f0e", width=2, dash="dash"),
    yaxis="y2"
))

# --- NEW: INVISIBLE DATA TRACE FOR TEXT POPUPS ---
# This trace map holds our text data. It remains invisible, but surfaces text data on mouse hover.
fig.add_trace(go.Scatter(
    x=df["Year"],
    y=[1] * len(df),  # Arbitrary y values since it's hidden from view
    name="Macro Event Note",
    mode="markers",
    marker=dict(opacity=0),  # Forces absolute invisibility on screen
    text=df["Historical_Event"],
    hovertemplate="%{text}<extra></extra>",  # Standardizes tooltip layout formatting
    hoverinfo="text"
))

# --- NEW: DRAW THE TRANSPARENT BACKGROUND COLUMNS ---
# Add the visual colored ranges directly into the layout architecture
for e in events:
    fig.add_vrect(
        x0=e["start"], x1=e["end"],
        fillcolor=e["color"],
        opacity=1,
        layer="below",  # Keeps colored rectangles sitting behind main graph lines
        line_width=0
    )

# Clean Layout Management Settings
fig.update_layout(
    xaxis_title="Timeline (Years)",
    yaxis_title="Total Market Index Base Value",
    xaxis=dict(tickmode="linear", dtick=10),
    yaxis=dict(
        title_font=dict(color="#1f77b4"),
        tickfont=dict(color="#1f77b4"),
        type="log"
    ),
    yaxis2=dict(
        title=dict(text="Annual Inflation Rate (%)", font=dict(color="#ff7f0e")),
        tickfont=dict(color="#ff7f0e"),
        anchor="x", overlaying="y", side="right", showgrid=False
    ),
    legend=dict(x=0.01, y=0.99, borderwidth=1),
    hovermode="x unified",  # Locks tooltips together vertically to show everything instantly
    height=650
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("### 🗒️ Data Overview Options")
show_data = st.checkbox("Toggle Raw Dataset Table")
if show_data:
    st.dataframe(df.style.format({"Market_Value": "{:,.2f}", "Inflation_Rate": "{:.2f}%"}), height=300)
