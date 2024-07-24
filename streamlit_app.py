import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import numpy as np
import pydeck as pdk

# Define API endpoints
API_ENDPOINTS = {
    "charts": "https://api.aviationapi.com/v1/charts",
    "airports": "https://api.aviationapi.com/v1/airports",
    "preferred_routes": "https://api.aviationapi.com/v1/preferred-routes",
    "weather_metar": "https://api.aviationapi.com/v1/weather/metar",
    "weather_taf": "https://api.aviationapi.com/v1/weather/taf",
    "vatsim_pilots": "https://api.aviationapi.com/v1/vatsim/pilots",
    "vatsim_controllers": "https://api.aviationapi.com/v1/vatsim/controllers",
}

# Streamlit Layout
st.title("Aviation Data Dashboard")

# Sidebar for user inputs
st.sidebar.header("User Inputs")

# API Selection
api_choice = st.sidebar.selectbox("Choose API", list(API_ENDPOINTS.keys()))

# Dynamic Inputs based on API choice
if api_choice in ["vatsim_pilots", "vatsim_controllers"]:
    airport_code = st.sidebar.text_input("Enter Airport Code (e.g., KATL)")
    departure_checkbox = st.sidebar.checkbox("Show Departures")
    arrival_checkbox = st.sidebar.checkbox("Show Arrivals")
elif api_choice in ["weather_metar", "weather_taf"]:
    airport_code = st.sidebar.text_input("Enter Airport Code (e.g., KAVL)")

# Fetch data from API
def fetch_data(endpoint, params=None):
    response = requests.get(API_ENDPOINTS[endpoint], params=params)
    return response.json()

# Display interactive table
def display_interactive_table(data):
    df = pd.DataFrame(data)
    st.dataframe(df)

# Plotting charts
def plot_charts(data):
    # Example data for plotting
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # Line Chart
    st.subheader("Line Chart")
    st.line_chart(pd.Series(y, index=x))

    # Area Chart
    st.subheader("Area Chart")
    st.area_chart(pd.Series(y, index=x))

    # Bar Chart
    st.subheader("Bar Chart")
    plt.figure(figsize=(10, 5))
    plt.bar(x[:10], y[:10])
    st.pyplot()

# Display Map
def display_map(data):
    # Example data for map
    if data:
        map_data = pd.DataFrame(data)
        st.pydeck_chart(pdk.Deck(
            initial_view_state=pdk.ViewState(
                latitude=map_data['latitude'].mean(),
                longitude=map_data['longitude'].mean(),
                zoom=11
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=map_data,
                    get_position=["longitude", "latitude"],
                    get_fill_color=[255, 0, 0, 140],
                    get_radius=200,
                )
            ],
        ))

# Button widget
if st.button("Fetch Data"):
    params = {
        "apt": airport_code,
        "dep": 1 if departure_checkbox else None,
        "arr": 1 if arrival_checkbox else None
    } if api_choice in ["vatsim_pilots", "vatsim_controllers"] else {
        "apt": airport_code
    }

    data = fetch_data(api_choice, params)

    if data:
        if isinstance(data, dict) and 'status' in data and data['status'] == 'error':
            st.error(f"Error: {data['message']}")
        else:
            display_interactive_table(data)
            plot_charts(data)
            display_map(data)
            st.success("Data fetched successfully!")
    else:
        st.warning("No data found.")

# Sidebar widgets
st.sidebar.subheader("Additional Widgets")
radio_option = st.sidebar.radio("Select Option", ["Option 1", "Option 2"])
selected_option = st.sidebar.selectbox("Choose an option", ["A", "B", "C"])
multiselect_options = st.sidebar.multiselect("Select multiple options", ["X", "Y", "Z"])
slider_value = st.sidebar.slider("Select a value", 0, 100, 50)
text_input = st.sidebar.text_input("Enter text")
number_input = st.sidebar.number_input("Enter a number", min_value=0, max_value=100, value=50)

st.sidebar.subheader("Information")
st.sidebar.info("This sidebar contains various widgets and settings.")
