import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def process_charts_data(data, group):
    if group not in data:
        st.error("No data available for the selected group.")
        return pd.DataFrame()
    
    group_data = data[group]
    
    if isinstance(group_data, dict):  # Handling case where group_data is a dictionary
        # Find the actual data list from the dictionary
        for key in group_data:
            group_data = group_data[key]
            break
    
    df = pd.DataFrame(group_data)
    return df

def plot_charts(df, group):
    if df.empty:
        st.info("No data to display.")
        return
    
    # Ensure that the DataFrame is not empty
    if not df.empty:
        st.subheader("Charts for Group: " + str(group))
        
        # Plotting a line chart
        st.subheader("Line Chart")
        if 'elevation' in df.columns:
            df['elevation'] = pd.to_numeric(df['elevation'], errors='coerce')
            st.line_chart(df[['elevation']])
        else:
            st.warning("Elevation data not available for line chart.")

        # Plotting an area chart
        st.subheader("Area Chart")
        if 'elevation' in df.columns:
            df['elevation'] = pd.to_numeric(df['elevation'], errors='coerce')
            st.area_chart(df[['elevation']])
        else:
            st.warning("Elevation data not available for area chart.")

        # Plotting a bar chart
        st.subheader("Bar Chart")
        if 'state_full' in df.columns and 'elevation' in df.columns:
            df['elevation'] = pd.to_numeric(df['elevation'], errors='coerce')
            state_elevation = df.groupby('state_full')['elevation'].mean()
            st.bar_chart(state_elevation)
        else:
            st.warning("State or elevation data not available for bar chart.")

def display_charts_data(data):
    st.sidebar.header("Charts Grouping")
    group = st.sidebar.selectbox("Select Chart Group", [1, 2, 3, 4, 5, 6, 7])

    charts_df = process_charts_data(data, group)
    
    if not charts_df.empty:
        st.subheader("Data Table for Group: " + str(group))
        st.dataframe(charts_df)
        
        plot_charts(charts_df, group)
    else:
        st.error("No data available to display.")

# Example usage
data = {
    # Your chart data here
}

display_charts_data(data)
