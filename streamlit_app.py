import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pydeck as pdk

# API Endpoints
AVIATION_API_BASE = "https://api.aviationapi.com/v1"

# Functions to Fetch Data
def fetch_airport_data(icao_code):
    response = requests.get(f"{AVIATION_API_BASE}/airports/{icao_code}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching airport data.")
        return {}

def fetch_weather_data(icao_code):
    response = requests.get(f"{AVIATION_API_BASE}/weather/metar?apt={icao_code}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching weather data.")
        return {}

def fetch_vatsim_pilots_data(icao_code):
    response = requests.get(f"{AVIATION_API_BASE}/vatsim/pilots?apt={icao_code}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching VATSIM pilots data.")
        return {}

def fetch_charts_data(icao_code):
    response = requests.get(f"{AVIATION_API_BASE}/charts?apt={icao_code}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching charts data.")
        return {}

def fetch_preferred_routes_data(icao_code):
    response = requests.get(f"{AVIATION_API_BASE}/preferred-routes?apt={icao_code}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching preferred routes data.")
        return {}

# Streamlit Application
st.title('Aviation Data Dashboard')

# Sidebar for User Inputs
st.sidebar.header('User Inputs')
icao_code = st.sidebar.text_input('Enter ICAO Code', 'KMIA')
show_charts = st.sidebar.checkbox('Show Charts')
show_weather = st.sidebar.checkbox('Show Weather')
show_pilots = st.sidebar.checkbox('Show VATSIM Pilots')
show_routes = st.sidebar.checkbox('Show Preferred Routes')

if icao_code:
    # Fetch and Display Airport Data
    airport_data = fetch_airport_data(icao_code)
    if airport_data:
        st.subheader(f"Airport Information: {airport_data.get('name', 'N/A')}")
        st.write(airport_data)

        # Map showing the airport location
        st.subheader('Airport Location Map')
        st.pydeck_chart(pdk.Deck(
            initial_view_state=pdk.ViewState(
                latitude=airport_data.get('latitude', 0),
                longitude=airport_data.get('longitude', 0),
                zoom=10,
                pitch=0
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=[{
                        'latitude': airport_data.get('latitude', 0),
                        'longitude': airport_data.get('longitude', 0)
                    }],
                    get_position=['longitude', 'latitude'],
                    get_color=[255, 0, 0],
                    get_radius=1000
                )
            ]
        ))

    # Fetch and Display Charts Data
    if show_charts:
        charts_data = fetch_charts_data(icao_code)
        if charts_data:
            st.subheader('Charts Data')
            st.write(charts_data)
            # Example chart - replace with actual data
            df_charts = pd.DataFrame(charts_data)
            st.line_chart(df_charts['value'])
            st.area_chart(df_charts['value'])
            st.bar_chart(df_charts['value'])

    # Fetch and Display Weather Data
    if show_weather:
        weather_data = fetch_weather_data(icao_code)
        if weather_data:
            st.subheader('Weather Data')
            st.write(weather_data)

    # Fetch and Display VATSIM Pilots Data
    if show_pilots:
        pilots_data = fetch_vatsim_pilots_data(icao_code)
        if pilots_data:
            st.subheader('VATSIM Pilots Data')
            st.write(pilots_data)

    # Fetch and Display Preferred Routes Data
    if show_routes:
        routes_data = fetch_preferred_routes_data(icao_code)
        if routes_data:
            st.subheader('Preferred Routes Data')
            st.write(routes_data)

# Add Widgets
st.sidebar.header('Widgets')
selected_option = st.sidebar.radio('Choose Widget', ['None', 'Slider', 'Text Input', 'Selectbox'])
if selected_option == 'Slider':
    slider_value = st.slider('Select a value', 0, 100, 25)
    st.write(f'Slider Value: {slider_value}')
elif selected_option == 'Text Input':
    text_input_value = st.text_input('Enter some text', 'Sample Text')
    st.write(f'Text Input Value: {text_input_value}')
elif selected_option == 'Selectbox':
    selectbox_value = st.selectbox('Choose an option', ['Option 1', 'Option 2', 'Option 3'])
    st.write(f'Selected Option: {selectbox_value}')

# Feedback and Message Boxes
st.success('This is a success message!')
st.info('This is an informational message!')
st.warning('This is a warning message!')
st.error('This is an error message!')

# Optionally, include a progress bar
st.subheader('Progress Bar')
progress = st.progress(0)
for i in range(100):
    progress.progress(i + 1)

# Optional Media Elements
st.subheader('Optional Media Elements')
st.image('https://example.com/image.png', caption='Sample Image')

# Layout Containers
with st.expander("Expand for more details"):
    st.write("Here are more details about the selected airport.")
