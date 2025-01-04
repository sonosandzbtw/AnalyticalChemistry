import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Title and description
st.title("Analytical Chemistry Tools")
st.write("This web app includes tools for titration curves and buffer pH calculations.")

# Sidebar for navigation
st.sidebar.title("Choose a Tool")
tool = st.sidebar.radio("Select an option:", ["Titration Curve Generator", "Buffer pH Calculator"])

# Titration Curve Generator
if tool == "Titration Curve Generator":
    st.header("Titration Curve Generator")
    
    # Input data for titration
    st.write("Enter titration data below:")
    initial_pH = st.number_input("Initial pH:", min_value=0.0, step=0.1)
    equivalence_volume = st.number_input("Volume at equivalence point (mL):", min_value=0.1, step=0.1)
    total_volume = st.number_input("Total volume of titrant added (mL):", min_value=0.1, step=0.1)
    
    if st.button("Generate Titration Curve"):
        try:
            # Generate example data for titration
            volumes = np.linspace(0, total_volume, 100)
            pH = initial_pH + np.log10(volumes / (equivalence_volume - volumes))  # Mock titration data

            # Plot the titration curve
            fig, ax = plt.subplots()
            ax.plot(volumes, pH, label="Titration Curve")
            ax.axvline(equivalence_volume, color='red', linestyle='--', label="Equivalence Point")
            ax.set_xlabel("Volume of Titrant (mL)")
            ax.set_ylabel("pH")
            ax.legend()
            st.pyplot(fig)
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Buffer pH Calculator
if tool == "Buffer pH Calculator":
    st.header("Buffer pH Calculator")
    
    # Input data for buffer calculation
    st.write("Enter buffer system details below:")
    pKa = st.number_input("Enter pKa of the acid:", min_value=0.0, step=0.01)
    acid_conc = st.number_input("Concentration of acid (HA):", min_value=0.0, step=0.01)
    base_conc = st.number_input("Concentration of base (A-):", min_value=0.0, step=0.01)
    
    if st.button("Calculate Buffer pH"):
        if acid_conc > 0 and base_conc > 0:
            pH = pKa + np.log10(base_conc / acid_conc)
            st.success(f"The pH of the buffer is: {pH:.2f}")
        else:
            st.error("Both acid and base concentrations must be greater than 0.")
