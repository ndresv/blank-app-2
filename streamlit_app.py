import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pydeck as pdk

# Function to fetch data from the API
def fetch_data(endpoint, params={}):
    url = f"https://api.aviationapi.com/v1/{endpoint}"
    response = requests.get(url, params=params)
    return response.json()

# Function to convert DMS to decimal
def dms_to_decimal(dms):
    degrees = float(dms[:dms.find('-')])
    minutes = float(dms[dms.find('-') + 1:dms.find('.')])
    seconds = float(dms[dms.find('.') + 1:])
    if dms[-1] in ['S', 'W']:
        return - (degrees + (minutes / 60) + (seconds / 3600))
    else:
        return degrees + (minutes / 60) + (seconds / 3600)

# Sidebar for selecting API option
st.sidebar.title("API Selection")
api_option = st.sidebar.radio("Choose API Option:", ["Airports", "Preferred Routes", "Weather", "VATSIM Pilots"])

if api_option == "Airports":
    icao_code = st.sidebar.text_input("Enter ICAO Code:", "KAVL")
    if st.sidebar.button("Fetch Airport Data"):
        airport_data = fetch_data("airports", {"icao": icao_code})
        
        # Extracting latitude and longitude
        latitude_dms = airport_data.get('latitude', '0-0-0N')
        longitude_dms = airport_data.get('longitude', '0-0-0W')
        latitude = dms_to_decimal(latitude_dms)
        longitude = dms_to_decimal(longitude_dms)

        # Display airport information
        st.subheader("Airport Information")
        st.write(f"Facility Name: {airport_data.get('facility_name')}")
        st.write(f"FAA Identifier: {airport_data.get('faa_ident')}")
        st.write(f"ICAO Identifier: {airport_data.get('icao_ident')}")
        st.write(f"Location: {airport_data.get('city')}, {airport_data.get('state_full')}")
        st.write(f"Elevation: {airport_data.get('elevation')} ft")
        
        # Map visualization
        st.subheader("Airport Location")
        map_data = pd.DataFrame({
            'latitude': [latitude],
            'longitude': [longitude]
        })
        st.map(map_data)
        
        # Interactive table of airport data
        st.subheader("Airport Data Table")
        st.dataframe(pd.DataFrame([airport_data]))

        # Charts (Line, Area, and Bar charts)
        st.subheader("Charts")
        
        # Line Chart Example
        st.write("Line Chart of Elevation Over Time (Dummy Data)")
        times = pd.date_range(start="2023-01-01", periods=10)
        elevations = np.random.randint(2000, 3000, size=10)
        line_chart_data = pd.DataFrame({"Time": times, "Elevation": elevations})
        st.line_chart(line_chart_data.set_index('Time'))

        # Area Chart Example
        st.write("Area Chart of Temperature Changes (Dummy Data)")
        temperatures = np.random.randint(60, 90, size=10)
        area_chart_data = pd.DataFrame({"Time": times, "Temperature": temperatures})
        st.area_chart(area_chart_data.set_index('Time'))

        # Bar Chart Example
        st.write("Bar Chart of Runway Lengths (Dummy Data)")
        runways = ["Runway 1", "Runway 2", "Runway 3"]
        lengths = np.random.randint(3000, 4000, size=3)
        bar_chart_data = pd.DataFrame({"Runway": runways, "Length": lengths})
        st.bar_chart(bar_chart_data.set_index('Runway'))

elif api_option == "Preferred Routes":
    st.sidebar.write("Feature Coming Soon")

elif api_option == "Weather":
    st.sidebar.write("Feature Coming Soon")

elif api_option == "VATSIM Pilots":
    st.sidebar.write("Feature Coming Soon")

# Widgets
st.sidebar.subheader("Additional Widgets")
st.sidebar.checkbox("Show Additional Information", value=True)

# Feedback and Messages
st.success("Application Loaded Successfully!")
st.info("Select an API option to get started.")
st.warning("Some features are still under development.")
st.error("If you encounter any issues, please contact support.")

# Extra Widgets
st.sidebar.radio("Select a Chart Type", ["Line", "Area", "Bar"])
st.sidebar.selectbox("Choose a Date", ["2024-07-23", "2024-08-01", "2024-08-15"])
st.sidebar.multiselect("Select Attributes", ["Elevation", "Temperature", "Runway Length"])
st.sidebar.slider("Set Time Range", min_value=1, max_value=24, value=(1, 12))
st.sidebar.text_input("Add Notes")
st.sidebar.number_input("Enter Value", value=10)
st.sidebar.date_input("Select Date")
st.sidebar.time_input("Select Time")

# Optional Progress Bar
with st.spinner("Loading data..."):
    # Simulating a long data loading process
    import time
    time.sleep(2)
