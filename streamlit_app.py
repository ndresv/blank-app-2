import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk

# Base URL for Aviation API
BASE_URL = "https://api.aviationapi.com/v1"

def fetch_data(endpoint):
    response = requests.get(f"{BASE_URL}/{endpoint}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data from {endpoint}")
        return None

# Define usability goals
st.title("Aviation Data Dashboard")

# Sidebar for navigation and interactive widgets
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Select an option", [
    "Airport Information",
    "Weather Information",
    "Charts",
    "Preferred Routes",
    "VATSIM Data"
])

if selection == "Airport Information":
    st.sidebar.subheader("Airport Info")
    airport_code = st.sidebar.text_input("Enter ICAO or IATA code", "KATL")
    
    if airport_code:
        data = fetch_data(f"airports/{airport_code}")
        if data:
            st.subheader(f"Information for Airport: {airport_code}")
            st.json(data)
            # Displaying data in a table
            df = pd.DataFrame([data])
            st.dataframe(df)

elif selection == "Weather Information":
    st.sidebar.subheader("Weather Info")
    airport_code = st.sidebar.text_input("Enter ICAO or IATA code for weather", "KATL")
    
    if airport_code:
        metar_data = fetch_data(f"weather/metar/{airport_code}")
        taf_data = fetch_data(f"weather/taf/{airport_code}")
        
        if metar_data and taf_data:
            st.subheader(f"Weather Data for Airport: {airport_code}")
            st.write("METAR Data")
            st.json(metar_data)
            st.write("TAF Data")
            st.json(taf_data)

elif selection == "Charts":
    st.sidebar.subheader("Charts")
    charts_data = fetch_data("charts")
    
    if charts_data:
        st.subheader("Charts Data")
        st.write(charts_data)

elif selection == "Preferred Routes":
    st.sidebar.subheader("Preferred Routes")
    preferred_routes_data = fetch_data("preferred-routes")
    
    if preferred_routes_data:
        st.subheader("Preferred Routes Data")
        st.write(preferred_routes_data)

elif selection == "VATSIM Data":
    st.sidebar.subheader("VATSIM Data")
    vatsim_pilots = fetch_data("vatsim/pilots")
    vatsim_controllers = fetch_data("vatsim/controllers")
    
    if vatsim_pilots and vatsim_controllers:
        st.subheader("VATSIM Pilots Data")
        st.write(vatsim_pilots)
        st.subheader("VATSIM Controllers Data")
        st.write(vatsim_controllers)

# Sample chart and map
st.subheader("Sample Visualization")
data = {
    "Airport": ["KATL", "KJFK", "KLAX"],
    "Flights": [1200, 1500, 1100]
}
df = pd.DataFrame(data)

st.write("Bar Chart of Flights")
st.bar_chart(df.set_index("Airport"))

# Map visualization
st.write("Sample Map")
map_data = pd.DataFrame({
    'lat': [33.6367, 40.6413, 33.9416],
    'lon': [-84.4279, -73.7781, -118.4085],
    'Airport': ["ATL", "JFK", "LAX"]
})
st.map(map_data)

# Widgets
if st.button("Show More Info"):
    st.info("Showing more detailed information.")

if st.checkbox("Show Map"):
    st.map(map_data)

# Success and error messages
st.success("Data successfully loaded.")
st.error("Error in loading data.")
