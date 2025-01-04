import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

st.title("Extended Calibration Curve Tool")
st.write("This tool generates calibration curves, calculates unknown concentrations, and performs basic statistical analysis.")

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

            # Unknown sample concentration
            unknown_absorbance = st.number_input("Enter absorbance of the unknown sample:", min_value=0.0, step=0.01)
            if unknown_absorbance > 0:
                unknown_concentration = (unknown_absorbance - intercept) / slope
                st.success(f"**Calculated Concentration for Unknown Sample**: {unknown_concentration:.4f} M")
    except ValueError:
        st.error("Invalid input. Please ensure all values are numbers.")
