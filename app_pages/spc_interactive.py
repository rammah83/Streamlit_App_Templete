import streamlit as st
import pandas as pd
import numpy as np
import src.pyspc.continous_interactive as spc  # Import the spc_plotly module


# main_streamlit_app.py
st.title('SPC Chart Generator with Plotly and Streamlit Forms')

# File uploader
col_left, col_right = st.columns([2,1], gap='medium')
uploaded_file = col_left.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx'])
if uploaded_file is not None:
    # Read the uploaded file
    try:
        file_type = uploaded_file.name.split('.')[-1].lower()
        if file_type == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_type in ['xls', 'xlsx']:
            df = pd.read_excel(uploaded_file)
        else:
            st.error('Unsupported file type.')
            st.stop()
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()
    col_right.success("File successfully uploaded!")
    with col_right.popover("Data Preview"):
        st.dataframe(df.head())
    columns = df.columns.tolist()

    # Create a form for user inputs
    with st.sidebar.form("spc_form"):
        st.markdown("### SPC Configuration")
        # Select column for analysis
        selected_column = st.selectbox('Select column for analysis', columns)
        # Input fields for subgroup size, LSL, USL
        num_samples = st.number_input(
            'Number per sample (subgroup size)',
            min_value=1, max_value=25, value=5, step=1
        )
        # Display default values based on data
        default_LSL = float(df[selected_column].min())
        default_USL = float(df[selected_column].max())
        LSL = st.number_input(
            'Lower Specification Limit (LSL)',
            value=default_LSL,
            step=0.1,
        )
        USL = st.number_input(
            'Upper Specification Limit (USL)',
            value=default_USL,
            step=0.1,
        )
        # Optional: Add validation to ensure LSL < USL
        if LSL >= USL:
            st.error("Error: LSL must be less than USL.")
            submitted = False
        else:
            # Submit button
            submitted = st.form_submit_button("Submit")
    if submitted:
        st.markdown("---")
        st.write("### SPC Analysis Results")
        # Prepare data for control charts
        data = df[selected_column].dropna()  # Remove NaN values if any
        # Decide which chart to plot based on num_samples
        if num_samples == 1:
            st.info('Using X-MR (Individuals and Moving Range) Chart since subgroup size is 1.')
            try:
                # Calculate control limits and statistics using spc_plotly functions
                X, X_bar, MR, MR_bar, UCL_X, LCL_X, UCL_MR, LCL_MR = spc.calculate_x_mr_chart(data)
                # Plot X chart with LSL and USL
                st.subheader('X (Individuals) Chart')
                fig1 = spc.plot_x_chart(X, UCL_X, LCL_X, X_bar, LSL=LSL, USL=USL)
                st.plotly_chart(fig1, use_container_width=True)
                # Plot MR chart (Specification limits may not be relevant here, but we'll include them for completeness)
                # st.subheader('Moving Range Chart')
                fig2 = spc.plot_mr_chart(MR, UCL_MR, LCL_MR, MR_bar, LSL=LSL, USL=USL)
                st.plotly_chart(fig2, use_container_width=True)
            except ValueError as e:
                st.error(e)
                st.stop()
        elif 2 <= num_samples <= 9:
            st.info('Using X-bar and R Chart since subgroup size is between 2 and 9.')
            try:
                # Calculate control limits and statistics using spc_plotly functions
                X_bar, X_double_bar, R, R_bar, UCL_X, LCL_X, UCL_R, LCL_R = spc.calculate_xbar_r_chart(data, num_samples)
                # Plot X-bar chart with LSL and USL
                # st.subheader('X-bar Chart')
                fig1 = spc.plot_xbar_chart(X_bar, UCL_X, LCL_X, X_double_bar, LSL=LSL, USL=USL)
                st.plotly_chart(fig1, use_container_width=True)
                # Plot R chart
                # st.subheader('R Chart')
                fig2 = spc.plot_r_chart(R, UCL_R, LCL_R, R_bar)
                st.plotly_chart(fig2, use_container_width=True)
            except ValueError as e:
                st.error(e)
                st.stop()
        elif num_samples >= 10:
            st.info('Using X-bar and S Chart since subgroup size is 10 or more.')
            try:
                # Calculate control limits and statistics using spc_plotly functions
                X_bar, X_double_bar, S, S_bar, UCL_X, LCL_X, UCL_S, LCL_S = spc.calculate_xbar_s_chart(data, num_samples)
                # Plot X-bar chart with LSL and USL
                # st.subheader('X-bar Chart')
                fig1 = spc.plot_xbar_chart(X_bar, UCL_X, LCL_X, X_double_bar, LSL=LSL, USL=USL)
                st.plotly_chart(fig1, use_container_width=True)
                # Plot S chart
                # st.subheader('S Chart')
                fig2 = spc.plot_s_chart(S, UCL_S, LCL_S, S_bar)
                st.plotly_chart(fig2, use_container_width=True)
            except ValueError as e:
                st.error(e)
                st.stop()
        else:
            st.error('Invalid subgroup size.')
       # Calculate process capability indices
        try:
            Cp, Cpk, Cpu, Cpl = spc.calculate_process_capability(data, LSL, USL)
            st.subheader('Process Capability Indices')

            # Determine process capability judgment
            if Cp >= 1.33 and Cpk >= 1.33:
                judgment = "Capable Process"
                color = "🟢"  # Green circle emoji
            elif Cp >= 1.00 and Cpk >= 1.00:
                judgment = "Marginally Capable Process"
                color = "🟠"  # Orange circle emoji
            else:
                judgment = "Not Capable Process"
                color = "🔴"  # Red circle emoji

            # Display judgment with color
            st.markdown(f"#### {color} **{judgment}**")
            # Display metrics in columns
            st.metric(label="Cp", value=f"{Cp:.2f}")
            st.metric(label="Cpk", value=f"{Cpk:.2f}")
            st.metric(label="Cpu", value=f"{Cpu:.2f}")
            st.metric(label="Cpl", value=f"{Cpl:.2f}")

        except Exception as e:
            st.error(f"Error calculating process capability indices: {e}")

else:
    col_left.info('Please upload a CSV or Excel file to get started.')
