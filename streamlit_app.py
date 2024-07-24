import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pydeck as pdk

# API Endpoints
API_ENDPOINTS = {
    'charts': 'https://api.aviationapi.com/v1/charts',
    'airports': 'https://api.aviationapi.com/v1/airports',
    'preferred_routes': 'https://api.aviationapi.com/v1/preferred-routes',
    'weather_metar': 'https://api.aviationapi.com/v1/weather/metar',
    'weather_taf': 'https://api.aviationapi.com/v1/weather/taf',
    'vatsim_pilots': 'https://api.aviationapi.com/v1/vatsim/pilots',
    'vatsim_controllers': 'https://api.aviationapi.com/v1/vatsim/controllers'
}

# Fetch data from API
def fetch_data(endpoint, params=None):
    response = requests.get(API_ENDPOINTS[endpoint], params=params)
    return response.json()

# Fetch data from APIs
charts_data = fetch_data('charts')
airports_data = fetch_data('airports')
preferred_routes_data = fetch_data('preferred_routes')
metar_data = fetch_data('weather_metar', {'apt': 'KAVL'})
taf_data = fetch_data('weather_taf', {'apt': 'KAVL'})
vatsim_pilots_data = fetch_data('vatsim_pilots', {'apt': 'KAVL'})
vatsim_controllers_data = fetch_data('vatsim_controllers', {'fac': 'CLT'})

# Streamlit app
st.title("Aviation Dashboard")

# Sidebar for API selection
st.sidebar.header("API Selection")
api_choice = st.sidebar.radio("Choose API Endpoint", list(API_ENDPOINTS.keys()))

# Display API data based on user selection
if api_choice == 'charts':
    st.subheader("Charts Data")
    st.write(charts_data)

elif api_choice == 'airports':
    st.subheader("Airports Data")
    df_airports = pd.DataFrame(airports_data)
    st.dataframe(df_airports)

elif api_choice == 'preferred_routes':
    st.subheader("Preferred Routes Data")
    df_routes = pd.DataFrame(preferred_routes_data)
    st.dataframe(df_routes)

elif api_choice == 'weather_metar':
    st.subheader("METAR Data")
    st.write(metar_data)

elif api_choice == 'weather_taf':
    st.subheader("TAF Data")
    st.write(taf_data)

elif api_choice == 'vatsim_pilots':
    st.subheader("VATSIM Pilots Data")
    df_pilots = pd.DataFrame(vatsim_pilots_data)
    st.dataframe(df_pilots)

elif api_choice == 'vatsim_controllers':
    st.subheader("VATSIM Controllers Data")
    df_controllers = pd.DataFrame(vatsim_controllers_data)
    st.dataframe(df_controllers)

# Interactive Table
st.subheader("Interactive Table")
df = pd.DataFrame({
    'Column 1': [1, 2, 3, 4],
    'Column 2': ['A', 'B', 'C', 'D']
})
st.dataframe(df)

# Charts
st.subheader("Charts")
chart_data = pd.DataFrame({
    'x': pd.date_range(start='2023-01-01', periods=10),
    'y1': range(10),
    'y2': [x**2 for x in range(10)]
})

st.line_chart(chart_data.set_index('x')['y1'], use_container_width=True)
st.area_chart(chart_data.set_index('x')[['y1', 'y2']], use_container_width=True)

# Map with points
st.subheader("Map")
map_data = pd.DataFrame({
    'lat': [37.7749, 34.0522, 40.7128],
    'lon': [-122.4194, -118.2437, -74.0060],
    'label': ['San Francisco', 'Los Angeles', 'New York']
})
st.map(map_data)

# Widgets
st.subheader("Widgets")
if st.button("Click Me"):
    st.success("Button clicked!")

show_message = st.checkbox("Show message", value=True)
if show_message:
    st.info("Checkbox is checked!")

# Additional widgets
st.radio("Choose one", ["Option 1", "Option 2", "Option 3"])
st.selectbox("Select an option", ["Option A", "Option B", "Option C"])
st.multiselect("Select multiple options", ["Option X", "Option Y", "Option Z"])
st.slider("Select a value", 0, 100, 50)
st.text_input("Enter text")
st.number_input("Enter a number", 0, 100, 25)
st.text_area("Enter a long text")
st.date_input("Select a date")
st.time_input("Select a time")
st.file_uploader("Upload a file")
st.color_picker("Pick a color")

# Error and Information messages
st.warning("This is a warning message.")
st.error("This is an error message.")

# Expanders
with st.expander("More Details"):
    st.write("Here are more details.")
