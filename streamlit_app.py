import streamlit as st
import requests
import pandas as pd

# API endpoints
API_ENDPOINTS = {
    'Airports': 'https://api.aviationapi.com/v1/airports?apt=',
    'Preferred Routes': 'https://api.aviationapi.com/v1/preferred-routes',
    'Weather METAR': 'https://api.aviationapi.com/v1/weather/metar?apt=',
    'VATSIM Pilots': 'https://api.aviationapi.com/v1/vatsim/pilots',
    'Charts': 'https://api.aviationapi.com/v1/charts?apt={icao}&group={group}'
}

# Grouping descriptions
CHART_GROUPS = {
    "2": "Airport Diagram only",
    "3": "General only",
    "4": "Departures only",
    "5": "Arrivals only",
    "6": "Approaches only",
}

# Function to fetch data from the API
def fetch_data(api_name, endpoint, params=None):
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from {api_name}: {e}")
        return None

# Function to display charts data
def display_charts_data(charts_data):
    st.header("Charts Data")
    if charts_data:
        st.write("Raw charts data:", charts_data)  # Debugging line
        for group in CHART_GROUPS.keys():
            if group in charts_data:
                st.subheader(f"Group: {CHART_GROUPS.get(group, 'Unknown Group')}")
                charts_df = pd.DataFrame(charts_data[group])
                st.write(f"{CHART_GROUPS.get(group, 'Unknown Group')} Table")
                st.dataframe(charts_df)
                
                # Example chart (customize based on your actual data)
                if not charts_df.empty:
                    st.line_chart(charts_df)
                    st.area_chart(charts_df)
                    st.bar_chart(charts_df)
            else:
                st.warning(f"Group {group} not found in the response.")
    else:
        st.warning("No charts data available.")

# Main app logic
st.title("Aviation Data Explorer")

api_option = st.sidebar.radio("Select API", list(API_ENDPOINTS.keys()))

if api_option == 'Airports':
    icao_code = st.text_input("Enter ICAO code (e.g., KMIA)")
    show_map = st.checkbox("Enable Map View", value=True)
    if st.button("Fetch Airport Data"):
        data = fetch_data(api_option, f"{API_ENDPOINTS['Airports']}{icao_code}")
        if data:
            airport = data.get(icao_code, [None])[0]  # Access the first airport in the list
            if airport:
                display_airport_data(airport, show_map)
            else:
                st.warning("Airport not found.")

elif api_option == 'Preferred Routes':
    if st.button("Fetch Preferred Routes Data"):
        data = fetch_data(api_option, API_ENDPOINTS['Preferred Routes'])
        display_preferred_routes(data)

elif api_option == 'Weather METAR':
    icao_code = st.text_input("Enter ICAO code (e.g., KMIA)")
    if st.button("Fetch Weather Data"):
        data = fetch_data(api_option, f"{API_ENDPOINTS['Weather METAR']}{icao_code}")
        display_weather_data(data)

elif api_option == 'VATSIM Pilots':
    if st.button("Fetch VATSIM Pilots Data"):
        data = fetch_data(api_option, API_ENDPOINTS['VATSIM Pilots'])
        display_vatsim_pilots(data)

elif api_option == 'Charts':
    icao_code = st.text_input("Enter ICAO code (e.g., KMIA)")
    group_description = st.selectbox("Select Chart Group", list(CHART_GROUPS.values()))
    group = [key for key, value in CHART_GROUPS.items() if value == group_description][0]
    st.write(f"Selected group: {group}")  # Debugging line
    if st.button("Fetch Charts Data"):
        data = fetch_data('Charts', API_ENDPOINTS['Charts'].format(icao=icao_code, group=group))
        display_charts_data(data)
