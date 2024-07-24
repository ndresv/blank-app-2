def display_charts_data(charts_data):
    st.header("Charts Data")
    
    if charts_data:
        for group, data in charts_data.items():
            st.subheader(f"Group: {group}")
            
            if group == '1' or group == '7':
                # Handle special cases for Group 1 and 7
                if isinstance(data, dict):
                    # Extract relevant part for Group 1
                    if 'General' in data:
                        data = data['General']
                    # Extract relevant part for Group 7
                    elif 'DP' in data:
                        data = data['DP']
                    else:
                        st.warning(f"Unexpected structure for Group {group}.")
                        continue
                else:
                    st.warning(f"Unexpected data type for Group {group}.")
                    continue
            else:
                data = charts_data[group]
            
            # Ensure the data is a list of dictionaries with consistent keys
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                try:
                    # Create DataFrame and handle inconsistent lengths
                    keys = data[0].keys()  # Extract all possible keys
                    # Ensure all rows have the same keys
                    consistent_data = [{key: row.get(key, None) for key in keys} for row in data]
                    charts_df = pd.DataFrame(consistent_data)
                    
                    st.write(f"{group} Table")
                    st.dataframe(charts_df)
                    
                    # Display charts (example, customize based on your data)
                    if 'value' in charts_df.columns:
                        st.line_chart(charts_df.set_index('state')['value'])
                        st.area_chart(charts_df.set_index('state')['value'])
                        st.bar_chart(charts_df.set_index('state')['value'])
                    else:
                        st.info(f"No 'value' column available for charts.")
                except Exception as e:
                    st.error(f"Error processing data for group {group}: {e}")
            else:
                st.warning(f"Data format is not as expected for group {group}.")
    else:
        st.warning("No charts data available.")
