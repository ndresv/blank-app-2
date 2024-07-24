import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pydeck as pdk

# Streamlit Page Configuration
st.set_page_config(page_title="Aviation Data Dashboard", layout="wide")

# Sidebar - API Options
st.sidebar.header("API Options")
api_option = st.sidebar.radio("Choose an API", ["Airports", "Weather", "VATSIM", "Charts", "Preferred Routes"])

# Function to fetch data from API
def fetch_data(api_url, params=None):
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

# Function to display interactive table
def display_interactive_table(data):
    df = pd.DataFrame(data)
    st.dataframe(df)

# Function to display line and area charts
def display_charts(data):
    df = pd.DataFrame(data)
    st.line_chart(df['value'])
    st.area_chart(df['value'])
    st.bar_chart(df['value'])

# Function to display map
def display_map(lat, lon):
    data = pd.DataFrame({
        'lat': [lat],
        'lon': [lon]
    })
    st.map(data)

# Airport data
if api_option == "Airports":
    st.header("Airport Data")
    airport_code = st.text_input("Enter ICAO or FAA code:")
    
    if airport_code:
        data = fetch_data(f"https://api.aviationapi.com/v1/airports?apt={airport_code}")
        if data:
            st.success(f"Data fetched for {airport_code}")
            display_interactive_table(data)

            # Map visualization
            lat = data[0]['latitude']
            lon = data[0]['longitude']
            display_map(lat, lon)

            # Display charts
            display_charts(data)

# Weather data
elif api_option == "Weather":
    st.header("Weather Data")
    airport_code = st.text_input("Enter ICAO code for METAR/TAF:")
    
    if airport_code:
        metar_data = fetch_data(f"https://api.aviationapi.com/v1/weather/metar?apt={airport_code}")
        taf_data = fetch_data(f"https://api.aviationapi.com/v1/weather/taf?apt={airport_code}")

        if metar_data:
            st.success(f"METAR data fetched for {airport_code}")
            st.json(metar_data)
        
        if taf_data:
            st.success(f"TAF data fetched for {airport_code}")
            st.json(taf_data)

# VATSIM data
elif api_option == "VATSIM":
    st.header("VATSIM Data")
    facility_code = st.text_input("Enter VATSIM facility code:")
    
    if facility_code:
        pilots_data = fetch_data(f"https://api.aviationapi.com/v1/vatsim/pilots?fac={facility_code}")
        controllers_data = fetch_data(f"https://api.aviationapi.com/v1/vatsim/controllers?fac={facility_code}")

        if pilots_data:
            st.success(f"VATSIM pilots data fetched for {facility_code}")
            display_interactive_table(pilots_data)
        
        if controllers_data:
            st.success(f"VATSIM controllers data fetched for {facility_code}")
            display_interactive_table(controllers_data)

# Charts data
elif api_option == "Charts":
    st.header("Charts Data")
    chart_code = st.text_input("Enter chart code:")
    
    if chart_code:
        data = fetch_data(f"https://api.aviationapi.com/v1/charts?apt={chart_code}")
        if data:
            st.success(f"Chart data fetched for {chart_code}")
            st.json(data)

# Preferred Routes data
elif api_option == "Preferred Routes":
    st.header("Preferred Routes Data")
    routes_data = fetch_data("https://api.aviationapi.com/v1/preferred-routes")
    if routes_data:
        st.success("Preferred routes data fetched")
        display_interactive_table(routes_data)
