import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Function to calculate pH
def calculate_pH(volume_base, acid_conc, base_conc, volume_acid):
    moles_acid = acid_conc * volume_acid / 1000  # Initial moles of acid
    moles_base = base_conc * volume_base / 1000  # Moles of base added
    
    if moles_base < moles_acid:  # Before equivalence point
        moles_H3O = moles_acid - moles_base
        pH = -np.log10(moles_H3O / (volume_acid + volume_base) * 1000)
    elif moles_base == moles_acid:  # At equivalence point
        pH = 7  # Neutral for strong acid and strong base
    else:  # After equivalence point
        moles_OH = moles_base - moles_acid
        pOH = -np.log10(moles_OH / (volume_acid + volume_base) * 1000)
        pH = 14 - pOH
        
    return pH

# Streamlit App
st.title("Interactive Titration Curve")

# Input fields
acid_concentration = st.slider("Acid Concentration (M)", 0.01, 1.0, 0.1, 0.01)
base_concentration = st.slider("Base Concentration (M)", 0.01, 1.0, 0.1, 0.01)
volume_acid = st.slider("Acid Volume (mL)", 10.0, 100.0, 50.0, 1.0)

# Calculate titration curve
volume_base_added = np.linspace(0, 2 * volume_acid, 500)
pH_values = [calculate_pH(vb, acid_concentration, base_concentration, volume_acid) for vb in volume_base_added]

# Create plot
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=volume_base_added,
    y=pH_values,
    mode='lines',
    name='Titration Curve'
))
equivalence_point = volume_acid * acid_concentration / base_concentration
fig.add_trace(go.Scatter(
    x=[equivalence_point, equivalence_point],
    y=[0, 14],
    mode='lines',
    name='Equivalence Point',
    line=dict(dash='dash', color='red')
))
fig.update_layout(
    title="Titration Curve",
    xaxis_title="Volume of Base Added (mL)",
    yaxis_title="pH",
    template="plotly_white"
)

st.plotly_chart(fig)
