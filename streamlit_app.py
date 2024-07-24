import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pydeck as pdk

# Function to convert coordinates
def convert_coordinates(degree, minutes, seconds, direction):
    decimal = float(degree) + float(minutes)/60 + float(seconds)/(60*60)
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

# Function to get airport data
def fetch_airport_data(icao_code):
    api_key = 'your_api_key'
    response = requests.get(f'https://api.aviationapi.com/v1/airports?apt={icao_code}', headers={'Authorization': f'Bearer {api_key}'})
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching data for ICAO code: {icao_code}")
        return None

# Function to fetch preferred routes
def fetch_preferred_routes():
    api_key = 'your_api_key'
    response = requests.get(f'https://api.aviationapi.com/v1/preferred-routes', headers={'Authorization': f'Bearer {api_key}'})
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching preferred routes data.")
        return None

# Function to fetch weather METAR data
def fetch_weather_metar(icao_code):
    api_key = 'your_api_key'
    response = requests.get(f'https://api.aviationapi.com/v1/weather/metar/{icao_code}', headers={'Authorization': f'Bearer {api_key}'})
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching METAR data for ICAO code: {icao_code}")
        return None

# Function to fetch VATSIM pilots data
def fetch_vatsim_pilots():
    api_key = 'your_api_key'
    response = requests.get(f'https://api.aviationapi.com/v1/vatsim/pilots', headers={'Authorization': f'Bearer {api_key}'})
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching VATSIM pilots data.")
        return None

# Streamlit app layout
st.title('Aviation Data Dashboard')

# Sidebar options
option = st.sidebar.selectbox('Select an API', ['Airports', 'Preferred Routes', 'Weather METAR', 'VATSIM Pilots'])

# Display content based on selection
if option == 'Airports':
    icao_code = st.text_input('Enter ICAO Code (e.g., KMIA)')
    if icao_code:
        airport_data = fetch_airport_data(icao_code)
        if airport_data:
            # Extract and convert coordinates
            latitude = convert_coordinates(*airport_data['latitude'].split('-')[1:], airport_data['latitude'][-1])
            longitude = convert_coordinates(*airport_data['longitude'].split('-')[1:], airport_data['longitude'][-1])
            
            # Display airport information
            st.write(pd.DataFrame([airport_data]))
            
            # Map visualization
            st.pydeck_chart(pdk.Deck(
                initial_view_state=pdk.ViewState(
                    latitude=latitude,
                    longitude=longitude,
                    zoom=12,
                    pitch=0
                ),
                layers=[
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=[{"position": [longitude, latitude], "size": 100}],
                        get_position="position",
                        get_fill_color=[255, 0, 0],
                        get_radius=1000
                    )
                ]
            ))
            
            # Fetch and display weather METAR
            weather_metar = fetch_weather_metar(icao_code)
            if weather_metar:
                st.write("Weather METAR Data:")
                st.json(weather_metar)

elif option == 'Preferred Routes':
    routes = fetch_preferred_routes()
    if routes:
        # Display interactive table
        st.write(pd.DataFrame(routes))
        # Display charts if needed

elif option == 'Weather METAR':
    icao_code = st.text_input('Enter ICAO Code for METAR (e.g., KMIA)')
    if icao_code:
        weather_metar = fetch_weather_metar(icao_code)
        if weather_metar:
            st.write(pd.DataFrame([weather_metar]))
            # Display charts based on METAR data

elif option == 'VATSIM Pilots':
    pilots = fetch_vatsim_pilots()
    if pilots:
        st.write(pd.DataFrame(pilots))
        # Display charts or other relevant data

# Adding widgets
if st.button('Refresh Data'):
    st.info('Refreshing data...')

st.checkbox('Show Detailed Data', value=True)
st.radio('Choose Chart Type', ['Line Chart', 'Area Chart', 'Bar Chart'])
st.selectbox('Select Airport', ['KMIA', 'KAVL', 'KORD'])
st.slider('Select Data Range', 0, 100, 50)
st.text_input('Search', 'Type here...')
st.date_input('Select Date', pd.to_datetime('today'))
