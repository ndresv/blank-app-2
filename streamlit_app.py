import streamlit as st
import pandas as pd
import requests
import json

def dms_to_dd(dms):
    """Convert DMS (Degrees, Minutes, Seconds) to Decimal Degrees."""
    degrees, minutes, seconds, direction = float(dms[:-1].split('-')[0]), float(dms.split('-')[1]), float(dms.split('-')[2]), dms[-1]
    dd = degrees + (minutes / 60) + (seconds / 3600)
    if direction in ['S', 'W']:
        dd *= -1
    return dd

def fetch_airport_data(icao):
    """Fetch data from the airport API."""
    api_url = f"https://api.aviationapi.com/v1/airports?apt={icao}"
    response = requests.get(api_url)
    return response.json()

def fetch_charts(icao, group):
    """Fetch charts data from the API."""
    api_url = f"https://api.aviationapi.com/v1/charts?apt={icao}&group={group}"
    response = requests.get(api_url)
    return response.json()

st.title("Airport Data and Charts")

# Checkbox for Map View
map_view_enabled = st.checkbox("Enable Map View", value=True)

# Input for ICAO Code
icao_code = st.text_input("Enter ICAO Code", "KMIA")

# Dropdown for Grouping Charts
group_option = st.selectbox(
    "Select Chart Group",
    options={
        1: "General, Departures, Arrivals, Approaches",
        2: "Airport Diagram only",
        3: "General only",
        4: "Departures only",
        5: "Arrivals only",
        6: "Approaches only",
        7: "Everything but General"
    }
)

# Fetch and Display Airport Data
if icao_code:
    airport_data = fetch_airport_data(icao_code)
    if airport_data:
        airport = airport_data.get(icao_code, [])[0]
        if airport:
            st.subheader(f"Airport Information for {icao_code}")
            st.write(f"Facility Name: {airport.get('facility_name')}")
            st.write(f"City: {airport.get('city')}")
            st.write(f"State: {airport.get('state')}")
            st.write(f"State Full: {airport.get('state_full')}")
            st.write(f"Latitude: {dms_to_dd(airport.get('latitude'))}")
            st.write(f"Longitude: {dms_to_dd(airport.get('longitude'))}")
            st.write(f"Control Tower: {airport.get('control_tower')}")
            # Add more fields as needed

            # If Map View is enabled
            if map_view_enabled:
                st.subheader("Map View")
                map_data = {
                    'Latitude': [dms_to_dd(airport.get('latitude'))],
                    'Longitude': [dms_to_dd(airport.get('longitude'))],
                    'Facility Name': [airport.get('facility_name')]
                }
                df_map = pd.DataFrame(map_data)
                st.map(df_map)

# Fetch and Display Charts Data
if icao_code and group_option:
    charts_data = fetch_charts(icao_code, group_option)
    if charts_data:
        st.subheader(f"Charts Data for {icao_code} (Group {group_option})")
        for group, group_name in {
            1: "General, Departures, Arrivals, Approaches",
            2: "Airport Diagram only",
            3: "General only",
            4: "Departures only",
            5: "Arrivals only",
            6: "Approaches only",
            7: "Everything but General"
        }.items():
            group_data = charts_data.get(str(group), [])
            if group_data:
                st.write(f"### {group_name}")
                df_group = pd.DataFrame(group_data)
                st.dataframe(df_group)
