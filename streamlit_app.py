import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk

# Function to fetch data from the API
def fetch_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching data: {response.status_code}")
        return None

# API URL (replace with actual endpoint and key if needed)
API_URL = "https://aviationapi.com/v1/"

# Streamlit layout
st.title("FAA Aeronautical Charts and Publications")

# Sidebar
st.sidebar.header("Filter Options")

# Interactive widgets
selected_option = st.sidebar.selectbox("Select Data", ["Airport Information", "Weather Data"])
date_input = st.sidebar.date_input("Select Date", pd.to_datetime("today"))

if selected_option == "Airport Information":
    # Fetch and display data for Airport Information
    airport_data = fetch_data(f"{API_URL}/airports")
    if airport_data:
        st.subheader("Airport Information")
        df = pd.DataFrame(airport_data)
        st.dataframe(df)
        
        # Display a bar chart for airport data
        st.subheader("Airport Data Bar Chart")
        st.bar_chart(df[['some_column']].set_index('some_index_column'))

elif selected_option == "Weather Data":
    # Fetch and display data for Weather Information
    weather_data = fetch_data(f"{API_URL}/weather")
    if weather_data:
        st.subheader("Weather Information")
        df = pd.DataFrame(weather_data)
        st.dataframe(df)
        
        # Display line and area charts for weather data
        st.subheader("Weather Data Charts")
        
        st.line_chart(df[['temperature', 'humidity']])
        st.area_chart(df[['precipitation']])
        
        # Display a map with weather data points
        st.subheader("Weather Data Map")
        st.pydeck_chart(pdk.Deck(
            initial_view_state=pdk.ViewState(latitude=37.7749, longitude=-122.4194, zoom=10),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=df,
                    get_position=["longitude", "latitude"],
                    get_color=[255, 0, 0],
                    get_radius=1000
                )
            ]
        ))

# Feedback and Messages
st.success("Data successfully loaded!")
st.info("Select an option from the sidebar to view data.")
st.warning("Ensure that API keys and endpoints are correctly configured.")
st.error("An error occurred while fetching data.")

# Optional: Add any other widgets if needed
radio_option = st.radio("Choose an option", ["Option 1", "Option 2"])
text_input = st.text_input("Enter some text")

# Display widgets
st.write("Radio Option Selected:", radio_option)
st.write("Text Input:", text_input)
