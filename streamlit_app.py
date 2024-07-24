import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pydeck as pdk

# Define API endpoints
API_BASE_URL = "https://api.aviationapi.com/v1"

# Function to make API requests
def fetch_data(endpoint, params=None):
    response = requests.get(f"{API_BASE_URL}/{endpoint}", params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error {response.status_code}: {response.json().get('message', 'Unknown error')}")
        return None

# Streamlit app
def main():
    st.title("Aviation Data Viewer")

    # Sidebar for navigation
    option = st.sidebar.selectbox("Choose an option", [
        "Charts",
        "Airports",
        "Preferred Routes",
        "Weather METAR",
        "Weather TAF",
        "VATSIM Pilots",
        "VATSIM Controllers"
    ])

    # Widgets
    st.sidebar.subheader("Filter Options")
    filter_choice = st.sidebar.radio("Select filter type:", ["None", "Departures", "Arrivals"])
    date_filter = st.sidebar.date_input("Select date:", pd.to_datetime("today"))

    if option == "Charts":
        st.header("Charts")
        icao = st.text_input("Enter ICAO Code (e.g., KATL)")
        if st.button("Fetch Charts"):
            data = fetch_data("charts", {"apt": icao})
            if data:
                st.json(data)
    
    elif option == "Airports":
        st.header("Airports")
        icao = st.text_input("Enter ICAO Code (e.g., KATL)")
        if st.button("Fetch Airport Data"):
            data = fetch_data("airports", {"apt": icao})
            if data:
                df = pd.DataFrame([data])
                st.dataframe(df)  # Interactive table
                st.success("Airport data fetched successfully!")
    
    elif option == "Preferred Routes":
        st.header("Preferred Routes")
        departure = st.text_input("Enter Departure ICAO (e.g., KATL)")
        arrival = st.text_input("Enter Arrival ICAO (e.g., KDFW)")
        if st.button("Fetch Preferred Routes"):
            data = fetch_data("preferred-routes", {"dep": departure, "arr": arrival})
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df)  # Interactive table
                st.info("Preferred routes data fetched successfully!")
    
    elif option == "Weather METAR":
        st.header("Weather METAR")
        icao = st.text_input("Enter ICAO Code (e.g., KAVL)")
        if st.button("Fetch METAR"):
            data = fetch_data("weather/metar", {"apt": icao})
            if data:
                st.json(data)
                # Line chart example
                df = pd.DataFrame(data['data'])  # Adjust based on actual data structure
                st.line_chart(df[['temp', 'wind_speed']])  # Example columns
    
    elif option == "Weather TAF":
        st.header("Weather TAF")
        icao = st.text_input("Enter ICAO Code (e.g., KAVL)")
        if st.button("Fetch TAF"):
            data = fetch_data("weather/taf", {"apt": icao})
            if data:
                st.json(data)
                # Area chart example
                df = pd.DataFrame(data['data'])  # Adjust based on actual data structure
                st.area_chart(df[['temp', 'wind_speed']])  # Example columns
    
    elif option == "VATSIM Pilots":
        st.header("VATSIM Pilots")
        airport = st.text_input("Enter Airport ICAO (e.g., KATL)")
        dep = st.checkbox("Show only departures")
        arr = st.checkbox("Show only arrivals")
        if st.button("Fetch VATSIM Pilots"):
            params = {
                "apt": airport,
                "dep": 1 if dep else None,
                "arr": 1 if arr else None
            }
            data = fetch_data("vatsim/pilots", params)
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df)  # Interactive table
                st.warning("VATSIM pilots data fetched successfully!")
    
    elif option == "VATSIM Controllers":
        st.header("VATSIM Controllers")
        facility = st.text_input("Enter Facility (e.g., CLT)")
        if st.button("Fetch VATSIM Controllers"):
            data = fetch_data("vatsim/controllers", {"fac": facility})
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df)  # Interactive table
                st.success("VATSIM controllers data fetched successfully!")
    
    # Example Map
    st.header("Map with Points")
    points = {
        'lat': [37.7749, 34.0522, 40.7128],
        'lon': [-122.4194, -118.2437, -74.0060],
        'label': ['San Francisco', 'Los Angeles', 'New York']
    }
    df_points = pd.DataFrame(points)
    st.map(df_points)

    # Example Bar Chart
    st.header("Example Bar Chart")
    df_bar = pd.DataFrame({
        'City': ['San Francisco', 'Los Angeles', 'New York'],
        'Value': [10, 20, 30]
    })
    st.bar_chart(df_bar.set_index('City'))

    # Example Progress Bar
    st.header("Progress Bar Example")
    with st.spinner("Loading..."):
        import time
        for i in range(100):
            time.sleep(0.05)
            st.progress(i + 1)

    # Example 3D Map
    st.header("3D Map Example")
    deck = pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=37.7749,
            longitude=-122.4194,
            zoom=11,
            pitch=50
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df_points,
                get_position=['lon', 'lat'],
                get_color=[255, 0, 0],
                get_radius=1000
            )
        ]
    )
    st.pydeck_chart(deck)

if __name__ == "__main__":
    main()
