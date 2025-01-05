import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import linregress

# Title
st.title("Analytical Chemistry Titration Curve Study Tool")

# Scenario Selection
st.sidebar.header("Titration Settings")
titration_type = st.sidebar.selectbox(
    "Select the titration type:",
    ["Strong Acid - Strong Base", "Weak Acid - Strong Base", "Weak Base - Strong Acid"]
)

# Data Input Section
st.subheader("Enter Your Titration Data")
st.write("Input your titration data below (Volume and pH):")

# Text area for data input
data = st.text_area(
    "Paste your data in two columns (Volume NaOH, pH), separated by commas.\nExample:\n0.000,3.58\n1.250,3.62\n2.000,3.72",
    height=200,
)

if data:
    try:
        # Split data into rows and columns
        data_rows = [line.split(",") for line in data.split("\n") if line.strip()]
        df = pd.DataFrame(data_rows, columns=["Volume NaOH (mL)", "pH"], dtype=float)
        
        # Display the table
        st.write("Your Titration Data:")
        st.write(df)

        # Plotting Titration Curve
        st.subheader("Titration Curve")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["Volume NaOH (mL)"],
            y=df["pH"],
            mode='markers+lines',
            name='Titration Curve'
        ))

        # Equivalence Point Calculation
        if len(df) > 1:
            max_slope = max(
                abs((df["pH"].iloc[i+1] - df["pH"].iloc[i]) / (df["Volume NaOH (mL)"].iloc[i+1] - df["Volume NaOH (mL)"].iloc[i]))
                for i in range(len(df)-1)
            )
            equivalence_index = [
                i for i in range(len(df)-1)
                if abs((df["pH"].iloc[i+1] - df["pH"].iloc[i]) / (df["Volume NaOH (mL)"].iloc[i+1] - df["Volume NaOH (mL)"].iloc[i])) == max_slope
            ][0]
            equivalence_point = df["Volume NaOH (mL)"].iloc[equivalence_index]
            equivalence_pH = df["pH"].iloc[equivalence_index]

            fig.add_trace(go.Scatter(
                x=[equivalence_point],
                y=[equivalence_pH],
                mode='markers',
                marker=dict(color='red', size=10),
                name='Equivalence Point'
            ))

            st.write(f"**Equivalence Point:** {equivalence_point:.3f} mL NaOH added, pH = {equivalence_pH:.2f}")

            # Half-Equivalence Point (for weak acids/bases)
            if titration_type in ["Weak Acid - Strong Base", "Weak Base - Strong Acid"]:
                half_eq_index = equivalence_index // 2
                half_eq_volume = df["Volume NaOH (mL)"].iloc[half_eq_index]
                half_eq_pH = df["pH"].iloc[half_eq_index]
                st.write(f"**Half-equivalence Point:** {half_eq_volume:.3f} mL NaOH, pH = {half_eq_pH:.2f}")
                st.write(f"**pKa (or pKb):** {half_eq_pH:.2f}")

        else:
            st.write("Not enough data points to calculate equivalence point.")

        # Detailed Explanations
        st.subheader("Detailed Explanations")
        st.markdown(f"""
        ### Key Features of Your Titration Curve:
        1. **Buffer Region**:
            - For **{titration_type}**, the buffer region occurs before the equivalence point.
            - The buffer region is characterized by a gradual change in pH due to the presence of the weak acid and its conjugate base (or vice versa).
            - Example: For weak acid-strong base, the weak acid (HA) reacts with NaOH to form its conjugate base (A⁻), which helps resist pH changes.

        2. **Half-Equivalence Point** (if applicable):
            - The half-equivalence point occurs when half of the weak acid (or weak base) has been neutralized.
            - At this point, the concentrations of the weak acid and its conjugate base are equal.
            - **pH = pKa** (for weak acid-strong base) or **pH = pKb** (for weak base-strong acid).

        3. **Equivalence Point**:
            - The equivalence point occurs when the moles of acid and base are stoichiometrically equal.
            - For **{titration_type}**, the equivalence point is expected at:
                - **pH = 7** for strong acid-strong base titration.
                - **pH > 7** for weak acid-strong base titration (due to the basic nature of the conjugate base).
                - **pH < 7** for weak base-strong acid titration (due to the acidic nature of the conjugate acid).

        4. **Post-Equivalence Point**:
            - Beyond the equivalence point, the pH is dominated by the excess strong acid or strong base added.
            - The curve levels off as the solution becomes saturated with the strong acid/base.

        ### Your Observations:
        - Equivalence Point: At {equivalence_point:.3f} mL, pH = {equivalence_pH:.2f}.
        """)

        fig.update_layout(
            title=f"Titration Curve: {titration_type}",
            xaxis_title="Volume of NaOH Added (mL)",
            yaxis_title="pH",
            template="plotly_white",
        )
        st.plotly_chart(fig)

        # Data Summary
        st.subheader("Data Summary and Calculations")
        if len(df) > 2:
            st.write("Summary of your data:")
            st.write(df.describe())

            # Perform linear regression on pH data
            slope, intercept, r_value, p_value, std_err = linregress(df["Volume NaOH (mL)"], df["pH"])
            st.write(f"Linear Regression p-value: {p_value:.5f}")
            st.write(f"Regression R-squared: {r_value**2:.5f}")
        else:
            st.write("Add more data points to see statistical summaries.")

    except Exception as e:
        st.error(f"Error processing data: {e}")
else:
    st.write("Waiting for data input...")
