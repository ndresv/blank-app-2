import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pydeck as pdk
from io import StringIO

# API endpoints
API_ENDPOINTS = {
    'Airports': 'https://api.aviationapi.com/v1/airports',
    'Preferred Routes': 'https://api.aviationapi.com/v1/preferred-routes',
    'Weather METAR': 'https://api.aviationapi.com/v1/weather/metar',
    'VATSIM Pilots': 'https://api.aviationapi.com/v1/vatsim/pilots'
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
    degrees, minutes, seconds, direction = float(dms[:-1].split('-')[0]), float(dms.split('-')[1]), float(dms.split('-')[2]), dms[-1]
    dd = degrees + minutes / 60 + seconds / 3600
    if direction in ['W', 'S']:
        dd *= -1
    return dd

# Function to display airport data
def display_airport_data(airport):
    st.header(f"Airport: {airport['facility_name']} ({airport['faa_ident']})")
    st.subheader(f"ICAO Code: {airport['icao_ident']}")
    st.write(f"City: {airport['city']}")
    st.write(f"State: {airport['state_full']}")
    st.write(f"Elevation: {airport['elevation']} feet")
    st.write(f"Control Tower: {airport['control_tower']}")
    st.write(f"UNICOM Frequency: {airport['unicom']}")
    
    # Convert latitude and longitude to decimal degrees
    lat_dd = dms_to_dd(airport['latitude'])
    lon_dd = dms_to_dd(airport['longitude'])
    
    st.map(pd.DataFrame({'lat': [lat_dd], 'lon': [lon_dd]}))

    # Interactive table
    st.write("Airport Data Table")
    st.dataframe(pd.DataFrame([airport]))

    # Charts (example data)
    chart_data = pd.DataFrame({
        'Attribute': ['Elevation', 'Control Tower'],
        'Value': [int(airport['elevation']), 1 if airport['control_tower'] == 'Y' else 0]
    })

    st.write("Charts")
    st.line_chart(chart_data['Value'])
    st.area_chart(chart_data['Value'])
    st.bar_chart(chart_data['Value'])

# Function to display preferred routes data
def display_preferred_routes(routes):
    st.header("Preferred Routes")
    if routes:
        routes_df = pd.DataFrame(routes)
        st.write("Preferred Routes Table")
        st.dataframe(routes_df)
    else:
        st.warning("No preferred routes available.")

# Function to display weather data
def display_weather_data(weather):
    st.header("Weather Data")
    if weather:
        st.write(weather)
    else:
        st.warning("No weather data available.")

# Function to display VATSIM pilots data
def display_vatsim_pilots(pilots):
    st.header("VATSIM Pilots")
    if pilots:
        pilots_df = pd.DataFrame(pilots)
        st.write("VATSIM Pilots Table")
        st.dataframe(pilots_df)
    else:
        st.warning("No VATSIM pilots data available.")

# Main app logic
st.title("Aviation Data Explorer")

api_option = st.sidebar.radio("Select API", list(API_ENDPOINTS.keys()))

if api_option == 'Airports':
    icao_code = st.text_input("Enter ICAO code (e.g., KAVL)")
    if st.button("Fetch Airport Data"):
        data = fetch_data(api_option, API_ENDPOINTS['Airports'], {'apt': icao_code})
        st.write(data)
        airport = data
        if airport:
            display_airport_data(airport)
        else:
            st.warning("Airport not found.")
                
elif api_option == 'Preferred Routes':
    st.button("Fetch Preferred Routes Data")
    data = fetch_data(api_option, API_ENDPOINTS['Preferred Routes'])
    display_preferred_routes(data)

elif api_option == 'Weather METAR':
    icao_code = st.text_input("Enter ICAO code (e.g., KAVL)")
    st.button("Fetch Weather Data")
    data = fetch_data(api_option, API_ENDPOINTS['Weather METAR'], {'icao': icao_code})
    display_weather_data(data)

elif api_option == 'VATSIM Pilots':
    st.button("Fetch VATSIM Pilots Data")
    data = fetch_data(api_option, API_ENDPOINTS['VATSIM Pilots'])
    display_vatsim_pilots(data)

st.sidebar.header("Additional Features")
show_expanded = st.sidebar.checkbox("Show Expanded")
if show_expanded:
    st.sidebar.info("Expanded features are shown.")
