import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Page config ---
st.set_page_config(page_title="AgriSense Simulator", layout="wide")
st.title("AgriSense Farming Advisory Simulator")

# --- User inputs ---
st.sidebar.header("Simulation Parameters")
days = st.sidebar.slider("Number of Days to Simulate", min_value=10, max_value=365, value=30)
initial_soil_moisture = st.sidebar.slider("Initial Soil Moisture (%)", min_value=10, max_value=100, value=50)
initial_temperature = st.sidebar.slider("Initial Temperature (°C)", min_value=10, max_value=45, value=25)

# --- Simulate data ---
np.random.seed(42)
temperature = initial_temperature + np.random.randn(days).cumsum()
soil_moisture = initial_soil_moisture + np.random.randn(days).cumsum()
rainfall = np.random.randint(0, 10, size=days)

df = pd.DataFrame({
    "Day": np.arange(1, days+1),
    "Temperature": temperature,
    "Soil Moisture": soil_moisture,
    "Rainfall": rainfall
})

st.subheader("Simulation Data")
st.dataframe(df)

# --- Plotting ---
st.subheader("Temperature & Soil Moisture Over Time")
fig, ax1 = plt.subplots(figsize=(10, 5))

ax1.plot(df["Day"], df["Temperature"], color='red', label='Temperature (°C)')
ax1.set_xlabel("Day")
ax1.set_ylabel("Temperature (°C)", color='red')
ax1.tick_params(axis='y', labelcolor='red')

ax2 = ax1.twinx()
ax2.plot(df["Day"], df["Soil Moisture"], color='blue', label='Soil Moisture (%)')
ax2.set_ylabel("Soil Moisture (%)", color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

fig.tight_layout()
st.pyplot(fig)

# --- Advisory ---
st.subheader("Farming Advisory")
if df["Soil Moisture"].iloc[-1] < 40:
    st.warning("Soil moisture is low. Consider irrigating crops.")
else:
    st.success("Soil moisture is sufficient.")

if df["Temperature"].max() > 35:
    st.warning("High temperature alert! Protect sensitive crops.")
