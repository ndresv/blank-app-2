import pandas as pd
import streamlit as st

def display_charts_data(charts_data):
    st.header("Charts Data")
    if charts_data:
        for group in charts_data.keys():
            st.subheader(f"Group: {group}")
            
            # Handle special cases for Group 1 and 7
            if group == '1' or group == '7':
                group_data = charts_data[group]
                if isinstance(group_data, dict):
                    # Handle nested structures for Group 1 and 7
                    if 'General' in group_data:
                        group_data = group_data['General']
                    elif 'DP' in group_data:
                        group_data = group_data['DP']
                    else:
                        st.warning(f"Unexpected structure for Group {group}.")
                        continue
                else:
                    st.warning(f"Unexpected data type for Group {group}.")
                    continue
            else:
                group_data = charts_data[group]
            
            # Convert to DataFrame
            try:
                charts_df = pd.DataFrame(group_data)
                st.write(f"{group} Table")
                st.dataframe(charts_df)

                # Example charts (customize based on your actual data)
                st.line_chart(charts_df.set_index('state')['value'])
                st.area_chart(charts_df.set_index('state')['value'])
                st.bar_chart(charts_df.set_index('state')['value'])
            except Exception as e:
                st.error(f"Error processing data for group {group}: {e}")
    else:
        st.warning("No charts data available.")
