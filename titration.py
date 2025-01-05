import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import linregress

# Title
st.title("Interactive Titration Curve with Explanations")

# Data Input Section
st.subheader("Enter Your Titration Data")
st.write("Input your titration data below (Volume and pH):")

# Text area for data input
data = st.text_area(
    "Paste your data in two columns (Volume NaOH, pH), separated by commas.\nExample:\n0.000,3.58\n1.250,3.62\n2.000,3.72",
    height=200,
)

# Parse the data into a DataFrame
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

        # Find Equivalence Point (approximation)
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

            fig.add_trace(go.Scatter(
                x=[equivalence_point],
                y=[df["pH"].iloc[equivalence_index]],
                mode='markers',
                marker=dict(color='red', size=10),
                name='Equivalence Point'
            ))

            st.write(f"**Equivalence Point Approximation:** {equivalence_point:.3f} mL NaOH added")
        else:
            st.write("Not enough data points to calculate equivalence point.")

        fig.update_layout(
            title="Titration Curve",
            xaxis_title="Volume of NaOH Added (mL)",
            yaxis_title="pH",
            template="plotly_white",
        )
        st.plotly_chart(fig)

        # Data Summary and Linear Regression
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

        # Academic Explanation
        st.markdown("""
        ### Key Concepts
        - **Equivalence Point**: This is where the moles of acid and base are stoichiometrically equal.
        - **Endpoint**: The observed point of neutralization. Ideally, this coincides with the equivalence point.
        - **Buffer Region**: In weak acid/base titrations, this is the region where pH changes gradually due to buffering.
        - **pKa**: For weak acids, the pKa can be approximated from the midpoint of the buffer region.
        - **Max Slope**: In a strong acid-base titration, the equivalence point corresponds to the steepest slope on the titration curve.
        """)
    except Exception as e:
        st.error(f"Error processing data: {e}")
else:
    st.write("Waiting for data input...")
