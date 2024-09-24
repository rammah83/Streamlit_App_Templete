import streamlit as st
import pandas as pd
import numpy as np
import src.pyspc.continous as pyspc
import matplotlib.pyplot as plt

st.title("Statistical Process Control")


st.title("SPC Chart Generator")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Read the uploaded file
    try:
        file_type = uploaded_file.name.split(".")[-1]
        if file_type == "csv":
            df = pd.read_csv(uploaded_file)
        elif file_type == "xlsx":
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file type.")
            st.stop()
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    with st.popover("Data Preview"):
        st.dataframe(df.head())

    # Select column for analysis
    columns = df.columns.tolist()
    with st.sidebar:
        selected_column = st.selectbox("Select column for analysis", columns)

        # Get slider inputs
        num_samples = st.slider(
            "Number of measurements per sample (subgroup size)",
            min_value=1,
            max_value=25,
            value=5,
        )
        LSL = st.number_input(
            "Lower Specification Limit", value=float(df[selected_column].min())
        )
        USL = st.number_input(
            "Upper Specification Limit", value=float(df[selected_column].max())
        )

        # Choose chart type
        chart_type = st.selectbox(
            "Select type of control chart", ["X-bar and R chart", "X-bar and S chart"]
        )

    # Prepare data for control charts
    data = df[selected_column]

    # Decide which chart to plot based on num_samples
    if num_samples == 1:
        st.write('Using X-MR (Individuals and Moving Range) Chart since subgroup size is 1.')
        try:
            # Calculate control limits and statistics using pyspc functions
            X, X_bar, MR, MR_bar, UCL_X, LCL_X, UCL_MR, LCL_MR = pyspc.calculate_x_mr_chart(data)

            # Plot X chart
            st.subheader('X (Individuals) Chart')
            fig1 = pyspc.plot_x_chart(X, UCL_X, LCL_X, X_bar)
            st.pyplot(fig1)

            # Plot MR chart
            st.subheader('Moving Range Chart')
            fig2 = pyspc.plot_mr_chart(MR, UCL_MR, LCL_MR, MR_bar)
            st.pyplot(fig2)
        except ValueError as e:
            st.error(e)
            st.stop()

    elif 2 <= num_samples <= 9:
        st.write('Using X-bar and R Chart since subgroup size is between 2 and 9.')
        try:
            # Calculate control limits and statistics using pyspc functions
            X_bar, X_double_bar, R, R_bar, UCL_X, LCL_X, UCL_R, LCL_R = pyspc.calculate_xbar_r_chart(data, num_samples)

            # Plot X-bar chart
            st.subheader('X-bar Chart')
            fig1 = pyspc.plot_xbar_chart(X_bar, UCL_X, LCL_X, X_double_bar)
            st.pyplot(fig1)

            # Plot R chart
            st.subheader('R Chart')
            fig2 = pyspc.plot_r_chart(R, UCL_R, LCL_R, R_bar)
            st.pyplot(fig2)
        except ValueError as e:
            st.error(e)
            st.stop()
    elif num_samples >= 10:
        st.write('Using X-bar and S Chart since subgroup size is 10 or more.')
        try:
            # Calculate control limits and statistics using pyspc functions
            X_bar, X_double_bar, S, S_bar, UCL_X, LCL_X, UCL_S, LCL_S = pyspc.calculate_xbar_s_chart(data, num_samples)

            # Plot X-bar chart
            st.subheader('X-bar Chart')
            fig1 = pyspc.plot_xbar_chart(X_bar, UCL_X, LCL_X, X_double_bar)
            st.pyplot(fig1)

            # Plot S chart
            st.subheader('S Chart')
            fig2 = pyspc.plot_s_chart(S, UCL_S, LCL_S, S_bar)
            st.pyplot(fig2)
        except ValueError as e:
            st.error(e)
            st.stop()

    else:
        st.error('Invalid subgroup size.')

    # Calculate process capability indices
    Cp, Cpk, Cpu, Cpl = pyspc.calculate_process_capability(data, LSL, USL)
    st.subheader('Process Capability Indices')
    st.write(f'Cp: {Cp:.4f}')
    st.write(f'Cpk: {Cpk:.4f}')
    st.write(f'Cpu: {Cpu:.4f}')
    st.write(f'Cpl: {Cpl:.4f}')

else:
    st.info('Please upload a CSV or Excel file to get started.')