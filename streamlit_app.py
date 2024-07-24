import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pydeck as pdk

# Function to fetch data from the APIs
def fetch_data(api_url, params):
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error {response.status_code}: Unable to fetch data")
        return None

# Function to convert DMS to Decimal Degrees
def dms_to_decimal(degrees, minutes, seconds, direction):
    decimal = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    if direction in ['S', 'W']:
        decimal *= -1
    return decimal

# Sidebar for API selection
st.sidebar.title("API Selection")
api_option = st.sidebar.selectbox("Select API", [
    "Airports",
    "Charts",
    "Preferred Routes",
    "Weather METAR",
    "Weather TAF",
    "VATSIM Pilots",
    "VATSIM Controllers"
])

# Function to display map for an airport
def display_airport_map(data):
    if data:
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        # Convert DMS to Decimal Degrees
        lat_deg, lat_min, lat_sec = map(float, latitude.split('-')[1:4])
        lon_deg, lon_min, lon_sec = map(float, longitude.split('-')[1:4])
        
        lat = dms_to_decimal(lat_deg, lat_min, lat_sec, latitude[-1])
        lon = dms_to_decimal(lon_deg, lon_min, lon_sec, longitude[-1])
        
        st.map(pd.DataFrame({
            'lat': [lat],
            'lon': [lon]
        }))
        
        st.success(f"Airport Map Displayed: {data.get('facility_name')}")

# Function to display interactive table
def display_interactive_table(data):
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)

# Function to display charts
def display_charts(data):
    if data:
        df = pd.DataFrame(data)
        
        # Line chart example
        st.line_chart(df[['latitude', 'longitude']])
        
        # Area chart example
        st.area_chart(df[['elevation']])
        
        # Bar chart example
        st.bar_chart(df[['elevation']])

# API call and data processing based on selection
if api_option == "Airports":
    icao_code = st.text_input("Enter ICAO Code for Airport (e.g., KAVL)")
    if icao_code:
        api_url = f"https://api.aviationapi.com/v1/airports"
        params = {"icao": icao_code}
        data = fetch_data(api_url, params)
        
        if data:
            display_airport_map(data)
            display_interactive_table([data])  # Assuming the data is a dict, wrap in list
            display_charts([data])  # Assuming the data is a dict, wrap in list

elif api_option == "Charts":
    # Add functionality for Charts
    st.info("Charts functionality not yet implemented.")

elif api_option == "Preferred Routes":
    # Add functionality for Preferred Routes
    st.info("Preferred Routes functionality not yet implemented.")

elif api_option == "Weather METAR":
    icao_code = st.text_input("Enter ICAO Code for METAR (e.g., KAVL)")
    if icao_code:
        api_url = f"https://api.aviationapi.com/v1/weather/metar"
        params = {"apt": icao_code}
        data = fetch_data(api_url, params)
        
        if data:
            st.write(data)
            st.success(f"METAR Data for {icao_code} displayed.")

elif api_option == "Weather TAF":
    icao_code = st.text_input("Enter ICAO Code for TAF (e.g., KAVL)")
    if icao_code:
        api_url = f"https://api.aviationapi.com/v1/weather/taf"
        params = {"apt": icao_code}
        data = fetch_data(api_url, params)
        
        if data:
            st.write(data)
            st.success(f"TAF Data for {icao_code} displayed.")

elif api_option == "VATSIM Pilots":
    apt_code = st.text_input("Enter Airport Identifier for VATSIM Pilots (e.g., KAVL)")
    if apt_code:
        api_url = f"https://api.aviationapi.com/v1/vatsim/pilots"
        params = {"apt": apt_code}
        data = fetch_data(api_url, params)
        
        if data:
            st.write(data)
            st.success(f"VATSIM Pilots Data for {apt_code} displayed.")

elif api_option == "VATSIM Controllers":
    fac_code = st.text_input("Enter Facility Identifier for VATSIM Controllers (e.g., CLT)")
    if fac_code:
        api_url = f"https://api.aviationapi.com/v1/vatsim/controllers"
        params = {"fac": fac_code}
        data = fetch_data(api_url, params)
        
        if data:
            st.write(data)
            st.success(f"VATSIM Controllers Data for {fac_code} displayed.")

# Additional widgets
if st.checkbox("Show Data Summary"):
    st.info("Data Summary will be displayed here.")
    # Display data summary or analysis if applicable

# Example of other widgets
if st.radio("Choose an option", ["Option 1", "Option 2"]) == "Option 1":
    st.write("You selected Option 1")

st.selectbox("Select a Value", ["Value 1", "Value 2", "Value 3"])
st.multiselect("Select Multiple Values", ["Value A", "Value B", "Value C"])
st.slider("Select a Range", 0, 100, (25, 75))
st.text_input("Enter some text")
st.number_input("Enter a number", min_value=0, max_value=100, value=50)
st.text_area("Enter detailed text")
st.date_input("Select a date")
st.time_input("Select a time")
st.file_uploader("Upload a file")
st.color_picker("Pick a color")
