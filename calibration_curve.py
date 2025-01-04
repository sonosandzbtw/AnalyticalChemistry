import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.stats import t

# Function to calculate statistics
def calculate_statistics(data):
    mean = np.mean(data)
    std_dev = np.std(data, ddof=1)  # Sample standard deviation (ddof=1)
    n = len(data)
    t_value = t.ppf(0.975, n - 1)  # 95% confidence interval
    margin_of_error = t_value * (std_dev / np.sqrt(n))
    return mean, std_dev, margin_of_error

# Initialize session state variables
if "slope" not in st.session_state:
    st.session_state.slope = None
if "intercept" not in st.session_state:
    st.session_state.intercept = None
if "calibration_done" not in st.session_state:
    st.session_state.calibration_done = False

# Center the title and description
st.markdown(
    """
    <div style="text-align: center; padding-top: 20px; padding-bottom: 20px;">
        <h1>Analytical Chemistry<br>Calibration Tool</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

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
            st.session_state.slope = model.coef_[0]
            st.session_state.intercept = model.intercept_
            r_squared = model.score(concentrations.reshape(-1, 1), absorbances)
            st.session_state.calibration_done = True

            # Calculate statistical metrics
            mean_absorbance, std_dev_absorbance, margin_of_error = calculate_statistics(absorbances)

            # Display results
            st.subheader("Statistical Analysis")
            st.write(f"**Mean**: {mean_absorbance:.4f}")
            st.write(f"**Standard Deviation**: {std_dev_absorbance:.4f}")
            st.write(f"**95% Confidence Interval**: ±{margin_of_error:.4f}")

            st.subheader("Calibration Curve")
            st.write(f"**Equation**: y = {st.session_state.slope:.4f}x + {st.session_state.intercept:.4f}")
            st.write(f"**R² Value**: {r_squared:.4f}")

            # Plot calibration curve
            fig, ax = plt.subplots()
            ax.scatter(concentrations, absorbances, label="Observed Data", color="blue")
            ax.plot(concentrations, model.predict(concentrations.reshape(-1, 1)), color="red", label="Regression Line")
            ax.set_xlabel("Concentration")
            ax.set_ylabel("Absorbance")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)
    except ValueError as e:
        st.error(f"Error: {e}. Please ensure all input values are numbers.")

# Calculate unknown sample concentration only if calibration is done
if st.session_state.calibration_done:
    st.write("Do you want to calculate the concentration of an unknown sample?")
    unknown_absorbance = st.number_input(
        "Enter absorbance of the unknown sample:",
        min_value=0.0,
        step=0.01,
    )

    if unknown_absorbance > 0:
        try:
            if st.session_state.slope == 0:
                st.error(
                    "Error: Cannot calculate concentration because the slope is zero (no valid calibration curve)."
                )
            else:
                unknown_concentration = (unknown_absorbance - st.session_state.intercept) / st.session_state.slope
                st.success(
                    f"**Calculated Concentration for Unknown Sample**: {unknown_concentration:.4f} M"
                )
        except ZeroDivisionError:
            st.error("Error: Division by zero occurred during the calculation.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
else:
    st.warning("Please generate the calibration curve first before entering an unknown absorbance.")
