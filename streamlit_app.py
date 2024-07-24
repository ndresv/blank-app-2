import streamlit as st
import requests
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt

# Function to fetch data from the API
def fetch_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching data: {response.status_code}")
        return None

# API URLs
CHARTS_API_URL = "https://api.aviationapi.com/v1/charts"
AIRPORTS_API_URL = "https://api.aviationapi.com/v1/airports"
PREFERRED_ROUTES_API_URL = "https://api.aviationapi.com/v1/preferred-routes"
WEATHER_API_URL = "https://api.aviationapi.com/v1/weather/metar"
VATSIM_API_URL = "https://api.aviationapi.com/v1/vatsim/pilots"

# Streamlit layout
st.title("FAA Aeronautical Charts and Publications")

# Sidebar
st.sidebar.header("Filter Options")

selected_option = st.sidebar.selectbox("Select Data", ["Airport Information", "Weather Data", "Preferred Routes", "VATSIM Data"])

if selected_option == "Airport Information":
    st.subheader("Airport Information")
    airport_data = fetch_data(AIRPORTS_API_URL)
    if airport_data:
        airport_df = pd.DataFrame(airport_data)
        st.dataframe(airport_df)
        
        # Display a bar chart for airport elevation data
        st.subheader("Airport Elevation Chart")
        st.bar_chart(airport_df[['elevation']])

elif selected_option == "Weather Data":
    st.subheader("Weather Information")
    weather_data = fetch_data(WEATHER_API_URL)
    if weather_data:
        weather_df = pd.DataFrame([weather_data])
        st.dataframe(weather_df)
        
        # Display line and area charts for weather data
        st.subheader("Weather Data Charts")
        st.line_chart(weather_df[['temp', 'dewpoint']])
        st.area_chart(weather_df[['visibility']])
        
        # Display a map with weather station
        st.subheader("Weather Station Map")
        st.pydeck_chart(pdk.Deck(
            initial_view_state=pdk.ViewState(latitude=35.0, longitude=-80.0, zoom=10),  # Use a default location
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=weather_df,
                    get_position=["longitude", "latitude"],
                    get_color=[255, 0, 0],
                    get_radius=1000
                )
            ]
        ))

elif selected_option == "Preferred Routes":
    st.subheader("Preferred Routes Information")
    preferred_routes_data = fetch_data(PREFERRED_ROUTES_API_URL)
    if preferred_routes_data:
        preferred_routes_df = pd.DataFrame(preferred_routes_data)
        st.dataframe(preferred_routes_df)
        
        # Display a bar chart for preferred route altitude data
        st.subheader("Preferred Routes Altitude Chart")
        st.bar_chart(preferred_routes_df[['altitude']])

elif selected_option == "VATSIM Data":
    st.subheader("VATSIM Data")
    vatsim_data = fetch_data(VATSIM_API_URL)
    if vatsim_data:
        vatsim_df = pd.DataFrame(vatsim_data)
        st.dataframe(vatsim_df)
        
        # Display a map with VATSIM flight data
        st.subheader("VATSIM Flight Map")
        st.pydeck_chart(pdk.Deck(
            initial_view_state=pdk.ViewState(latitude=32.30375, longitude=-94.69470, zoom=5),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=vatsim_df,
                    get_position=["longitude", "latitude"],
                    get_color=[0, 0, 255],
                    get_radius=1000
                )
            ]
        ))

# Feedback and Messages
st.success("Data successfully loaded!")
st.info("Select an option from the sidebar to view data.")
st.warning("Ensure that API endpoints are correctly configured.")
st.error("An error occurred while fetching data.")

# Additional Widgets
radio_option = st.radio("Choose an option", ["Option 1", "Option 2"])
text_input = st.text_input("Enter some text")

# Display widgets
st.write("Radio Option Selected:", radio_option)
st.write("Text Input:", text_input)
