import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
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

# Function to convert DMS to decimal degrees
def dms_to_decimal(degrees, minutes, seconds, direction):
    decimal = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

# Function to process the airport data
def process_airport_data(data):
    # Extract and convert latitude and longitude
    lat_dms = data['latitude'].split('-')
    lon_dms = data['longitude'].split('-')
    latitude = dms_to_decimal(lat_dms[0], lat_dms[1], lat_dms[2][:-1], lat_dms[2][-1])
    longitude = dms_to_decimal(lon_dms[0], lon_dms[1], lon_dms[2][:-1], lon_dms[2][-1])
    return latitude, longitude

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
                # Example of an interactive table
                df = pd.DataFrame(data)
                st.dataframe(df)
                st.success("Charts data fetched successfully!")

                # Example Line Chart
                if 'charts' in data:
                    df_charts = pd.DataFrame(data['charts'])
                    st.line_chart(df_charts[['altitude', 'heading']])  # Adjust columns as needed
                
                # Example Area Chart
                if 'weather' in data:
                    df_weather = pd.DataFrame(data['weather'])
                    st.area_chart(df_weather[['temperature', 'wind_speed']])  # Adjust columns as needed
    
    elif option == "Airports":
        st.header("Airports")
        icao = st.text_input("Enter ICAO Code (e.g., KMIA)")
        if st.button("Fetch Airport Data"):
            data = fetch_data("airports", {"apt": icao})
            if data:
                latitude, longitude = process_airport_data(data)
                
                df = pd.DataFrame([data])
                st.dataframe(df)  # Interactive table
                st.success("Airport data fetched successfully!")

                # Example Map
                airport_location = {
                    'lat': [latitude],
                    'lon': [longitude],
                    'label': [data['facility_name']]
                }
                df_location = pd.DataFrame(airport_location)
                st.pydeck_chart(pdk.Deck(
                    initial_view_state=pdk.ViewState(
                        latitude=latitude,
                        longitude=longitude,
                        zoom=11,
                        pitch=50
                    ),
                    layers=[
                        pdk.Layer(
                            'ScatterplotLayer',
                            data=df_location,
                            get_position=['lon', 'lat'],
                            get_color=[255, 0, 0],
                            get_radius=1000
                        )
                    ]
                ))

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

                # Example Bar Chart
                if not df.empty:
                    st.bar_chart(df.set_index('route_id')['distance'])

    elif option == "Weather METAR":
        st.header("Weather METAR")
        icao = st.text_input("Enter ICAO Code (e.g., KAVL)")
        if st.button("Fetch METAR"):
            data = fetch_data("weather/metar", {"apt": icao})
            if data:
                st.json(data)
                # Example Line Chart for METAR data
                if 'temperature' in data:
                    df_temp = pd.DataFrame(data['temperature'])
                    st.line_chart(df_temp[['temperature']])

    elif option == "Weather TAF":
        st.header("Weather TAF")
        icao = st.text_input("Enter ICAO Code (e.g., KAVL)")
        if st.button("Fetch TAF"):
            data = fetch_data("weather/taf", {"apt": icao})
            if data:
                st.json(data)
                # Example Area Chart for TAF data
                if 'wind_speed' in data:
                    df_taf = pd.DataFrame(data['wind_speed'])
                    st.area_chart(df_taf[['wind_speed']])

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

                # Example Map for VATSIM Pilots
                if not df.empty:
                    st.pydeck_chart(pdk.Deck(
                        initial_view_state=pdk.ViewState(
                            latitude=df['lat'].mean(),
                            longitude=df['lon'].mean(),
                            zoom=10,
                            pitch=50
                        ),
                        layers=[
                            pdk.Layer(
                                'ScatterplotLayer',
                                data=df,
                                get_position=['lon', 'lat'],
                                get_color=[0, 0, 255],
                                get_radius=500
                            )
                        ]
                    ))

    elif option == "VATSIM Controllers":
        st.header("VATSIM Controllers")
        facility = st.text_input("Enter Facility (e.g., CLT)")
        if st.button("Fetch VATSIM Controllers"):
            data = fetch_data("vatsim/controllers", {"fac": facility})
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df)  # Interactive table
                st.success("VATSIM controllers data fetched successfully!")

if __name__ == "__main__":
    main()
