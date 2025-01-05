import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Title
st.title("Interactive Titration Curve")

# Data Input Section
st.header("Enter Titration Data")
st.write("Input your titration data below (Volume and pH):")

# Create columns for data entry
data = st.text_area("Paste your data in two columns (Volume NaOH, pH), separated by commas.\nExample:\n0.000,3.58\n1.250,3.62", height=200)

# Parse the data into a DataFrame
if data:
    try:
        # Split data into rows and columns
        data_rows = [line.split(",") for line in data.split("\n") if line.strip()]
        df = pd.DataFrame(data_rows, columns=["Volume (mL)", "pH"], dtype=float)
        
        # Display the table
        st.write("Your Titration Data:")
        st.write(df)
        
        # Generate Plot
        st.header("Titration Curve")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["Volume (mL)"],
            y=df["pH"],
            mode='markers+lines',
            name='Titration Curve'
        ))
        
        fig.update_layout(
            title="Titration Curve (Custom Data)",
            xaxis_title="Volume of NaOH Added (mL)",
            yaxis_title="pH",
            template="plotly_white"
        )
        
        st.plotly_chart(fig)
        
    except Exception as e:
        st.error(f"Error processing data: {e}")
else:
    st.write("Waiting for data input...")
