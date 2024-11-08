# Streamlit-based PPD Data Explorer

import streamlit as st
import pandas as pd
import numpy as np

# Define function to read the PPD file
def read_ppd_file(file):
    try:
        # Assuming the PPD file is a tab-separated CSV format
        df = pd.read_csv(file, sep='\t')
    except Exception as e:
        st.error(f"Error reading file: {e}")
        df = pd.DataFrame()
    return df

# Define main UI and functionalities
def main():
    st.title("PPD File Data Explorer")

    # File upload
    uploaded_file = st.file_uploader("Upload your PPD file", type=["ppd"])

    if uploaded_file is not None:
        # Load data
        df = read_ppd_file(uploaded_file)
        if not df.empty:
            st.success("File successfully loaded!")
            
            # Display data preview
            st.subheader("Data Preview")
            st.write(df.head())

            # Column selection for exploration
            st.subheader("Column Selection")
            selected_columns = st.multiselect("Select columns to explore", df.columns.tolist(), default=df.columns.tolist())
            if selected_columns:
                st.write("Selected Columns Data:")
                st.write(df[selected_columns])

                # Basic statistics
                st.subheader("Basic Statistics")
                stats = df[selected_columns].describe()
                st.write(stats)

            # Custom calculation options
            st.subheader("Custom Calculations")

            # Mean calculation
            if st.checkbox("Calculate Mean"):
                st.write(df[selected_columns].mean())

            # Median calculation
            if st.checkbox("Calculate Median"):
                st.write(df[selected_columns].median())

            # Standard deviation calculation
            if st.checkbox("Calculate Standard Deviation"):
                st.write(df[selected_columns].std())

            # Filtering options
            st.subheader("Filtering Options")
            filter_column = st.selectbox("Select a column to filter by", df.columns)
            if filter_column:
                min_val, max_val = st.slider("Set range for filtering", float(df[filter_column].min()), float(df[filter_column].max()), (float(df[filter_column].min()), float(df[filter_column].max())))
                filtered_data = df[(df[filter_column] >= min_val) & (df[filter_column] <= max_val)]
                st.write("Filtered Data")
                st.write(filtered_data)

            # Export filtered data as CSV
            st.subheader("Export Filtered Data")
            if st.button("Export to CSV"):
                filtered_data.to_csv("filtered_data.csv", index=False)
                st.success("Filtered data exported as 'filtered_data.csv'")

# Run the app
if __name__ == "__main__":
    main()
