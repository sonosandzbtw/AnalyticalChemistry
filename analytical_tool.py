import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Title and description
st.title("Analytical Chemistry Tools")
st.write("This web app includes tools for calibration curves, titration curves, and buffer pH calculations.")

# Sidebar for navigation
st.sidebar.title("Choose a Tool")
tool = st.sidebar.radio("Select a tool:", ["Calibration Curve Tool", "Titration Curve Generator", "Buffer pH Calculator"])

# Calibration Curve Tool
if tool == "Calibration Curve Tool":
    st.header("Calibration Curve Tool")
    
    # Input concentrations and absorbances
    concentration_input = st.text_input("Enter known concentrations (comma-separated):", "0.1, 0.2, 0.3, 0.4, 0.5")
    absorbance_input = st.text_input("Enter corresponding absorbance values (comma-separated):", "0.05, 0.1, 0.15, 0.21, 0.25")
    
    if st.button("Generate Calibration Curve"):
        try:
            # Parse input data
            concentrations = np.array([float(x.strip()) for x in concentration_input.split(",")])
            absorbances = np.array([float(x.strip()) for x in absorbance_input.split(",")])
            
            if len(concentrations) != len(absorbances):
                st.error("Error: The number of concentrations and absorbances must match.")
            else:
                # Perform linear regression
                model = LinearRegression()
                model.fit(concentrations.reshape(-1, 1), absorbances)
                slope = model.coef_[0]
                intercept = model.intercept_
                r_squared = model.score(concentrations.reshape(-1, 1), absorbances)

                # Display results
                st.success(f"**Calibration Curve Equation**: y = {slope:.4f}x + {intercept:.4f}")
                st.success(f"**R² Value**: {r_squared:.4f}")

                # Plot calibration curve
                fig, ax = plt.subplots()
                ax.scatter(concentrations, absorbances, label="Observed Data", color="blue")
                ax.plot(concentrations, model.predict(concentrations.reshape(-1, 1)), color="red", label="Regression Line")
                ax.set_xlabel("Concentration")
                ax.set_ylabel("Absorbance")
                ax.legend()
                ax.grid(True)
                st.pyplot(fig)

                # Unknown concentration calculation
                unknown_absorbance = st.number_input("Enter absorbance of the unknown sample:", min_value=0.0, step=0.01)
                if unknown_absorbance > 0:
                    unknown_concentration = (unknown_absorbance - intercept) / slope
                    st.success(f"**Calculated Concentration for Unknown Sample**: {unknown_concentration:.4f} M")
        except Exception as e:
            st.error(f"An error occurred: {e}")

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
