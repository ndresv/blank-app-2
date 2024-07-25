import streamlit as st
import requests
import pandas as pd

# API endpoints
API_ENDPOINTS = {
    'Airports': 'https://api.aviationapi.com/v1/airports?apt=',
    'Preferred Routes': 'https://api.aviationapi.com/v1/preferred-routes',
    'VATSIM Pilots': 'https://api.aviationapi.com/v1/vatsim/pilots?apt=',
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

# Convert DMS to Decimal Degrees
def dms_to_dd(dms):
    parts = dms[:-1].split('-')
    degrees = float(parts[0])
    minutes = float(parts[1])
    seconds = float(parts[2])
    direction = dms[-1]
    
    dd = degrees + minutes / 60 + seconds / 3600
    if direction in ['W', 'S']:
        dd *= -1
    return dd

# Function to display airport data
def display_airport_data(airport, show_map):
    st.header(f"Airport: {airport.get('facility_name', 'N/A')} ({airport.get('faa_ident', 'N/A')})")
    st.subheader(f"ICAO Code: {airport.get('icao_ident', 'N/A')}")
    st.write(f"City: {airport.get('city', 'N/A')}")
    st.write(f"State: {airport.get('state_full', 'N/A')}")
    st.write(f"Elevation: {airport.get('elevation', 'N/A')} feet")
    st.write(f"Control Tower: {airport.get('control_tower', 'N/A')}")
    st.write(f"UNICOM Frequency: {airport.get('unicom', 'N/A')}")

    if show_map:
        # Convert latitude and longitude to decimal degrees
        lat_dd = dms_to_dd(airport.get('latitude', '0-0-0.0N'))
        lon_dd = dms_to_dd(airport.get('longitude', '0-0-0.0E'))

        st.map(pd.DataFrame({'lat': [lat_dd], 'lon': [lon_dd]}))

    # Interactive table
    st.write("Airport Data Table")
    st.dataframe(pd.DataFrame([airport]))

    # Charts (example data)
    chart_data = pd.DataFrame({
        'Attribute': ['Elevation', 'Control Tower'],
        'Value': [int(airport.get('elevation', 0)), 1 if airport.get('control_tower', 'N') == 'Y' else 0]
    })

# Function to display charts data
def display_charts_data(charts_data):
    if charts_data:
        for group in charts_data.keys():
            charts_df = pd.DataFrame(charts_data[group])
            st.dataframe(charts_df)
    else:
        st.warning("No charts data available.")

# Function to display preferred routes data
def display_preferred_routes(routes):
    st.header("Preferred Routes")
    if routes:
        routes_df = pd.DataFrame(routes)
        st.write("Preferred Routes Table")
        st.dataframe(routes_df)
    else:
        st.warning("No preferred routes available.")

def display_vatsim_pilots(pilots):
    st.header("VATSIM Pilots")
    
    if pilots:
        # Extract airport key
        airport_key = list(pilots.keys())[0]
        airport_data = pilots[airport_key]
        
        # Handle Departures
        if 'Departures' in airport_data:
            departures = airport_data['Departures']
            if departures:
                departures_df = pd.DataFrame(departures)
                st.write("Departures")
                st.dataframe(departures_df)
            else:
                st.write("No departure data available.")
        
        # Handle Arrivals
        if 'Arrivals' in airport_data:
            arrivals = airport_data['Arrivals']
            if arrivals:
                arrivals_df = pd.DataFrame(arrivals)
                st.write("Arrivals")
                st.dataframe(arrivals_df)
            else:
                st.write("No arrival data available.")
    else:
        st.warning("No VATSIM pilots data available.")

# Function to compare two airports
def compare_airports(airport1, airport2):
    if airport1 and airport2:
        st.header("Compare Airports")
        
        # Create a dataframe for comparison
        comparison_data = {
            'Airport': [airport1.get('icao_ident', 'Airport 1'), airport2.get('icao_ident', 'Airport 2')],
            'Elevation': [int(airport1.get('elevation', 0)), int(airport2.get('elevation', 0))]
        }
        comparison_df = pd.DataFrame(comparison_data).set_index('Airport')
        
        # Display bar chart for comparison
        st.write("Elevation Comparison")
        st.bar_chart(comparison_df)
        
        st.write("Comparison Data Table")
        st.dataframe(comparison_df)
    else:
        st.warning("Both airports must be selected for comparison.")

# Main app logic
st.title("Aviation Data Explorer")

api_option = st.sidebar.radio("Select API", list(API_ENDPOINTS.keys()))

if api_option == 'Airports':
    icao_code1 = st.text_input("Enter first ICAO code (e.g., KMIA)")
    icao_code2 = st.text_input("Enter second ICAO code (optional for comparison)")
    show_map = st.checkbox("Enable Map View", value=True)
    if st.button("Fetch Airport Data"):
        data1 = fetch_data(api_option, f"{API_ENDPOINTS['Airports']}{icao_code1}")
        airport1 = data1.get(icao_code1, [None])[0] if data1 else None
        
        if icao_code2:
            data2 = fetch_data(api_option, f"{API_ENDPOINTS['Airports']}{icao_code2}")
            airport2 = data2.get(icao_code2, [None])[0] if data2 else None
        else:
            airport2 = None
        
        if airport1:
            display_airport_data(airport1, show_map)
            st.Success("First airport found!")
        else:
            st.warning("First airport not found!")
        
        if airport2:
            display_airport_data(airport2, show_map)
            st.Success("Second airport found!")
        else:
            st.warning("Second airport not found!")
        
        if airport1 and airport2:
            compare_airports(airport1, airport2)

elif api_option == 'Preferred Routes':
    if st.button("Fetch Preferred Routes Data"):
        data = fetch_data(api_option, API_ENDPOINTS['Preferred Routes'])
        display_preferred_routes(data)

elif api_option == 'VATSIM Pilots':
    icao_code = st.text_input("Enter ICAO code (e.g., KMIA)")
    if st.button("Fetch VATSIM Pilots Data"):
        data = fetch_data(api_option, f"{API_ENDPOINTS['VATSIM Pilots']}{icao_code}")
        display_vatsim_pilots(data)

elif api_option == 'Charts':
    icao_code = st.text_input("Enter ICAO code (e.g., KMIA)")
    group_description = st.selectbox("Select Chart Group", list(CHART_GROUPS.values()))
    group = [key for key, value in CHART_GROUPS.items() if value == group_description][0]
    if st.button("Fetch Charts Data"):
        data = fetch_data('Charts', API_ENDPOINTS['Charts'].format(icao=icao_code, group=group))
        st.header("Charts Data")
        st.subheader(f"Group: {CHART_GROUPS.get(group, 'Unknown Group')}")
        display_charts_data(data)
