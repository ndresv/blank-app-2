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

# Function to convert latitude and longitude to decimal
def convert_to_decimal(degree, minute, direction):
    decimal = float(degree) + float(minute) / 60
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

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
                # Debugging: Inspect the data
                st.write("Charts data:", data)
                
                df = pd.DataFrame(data)
                st.dataframe(df)

                # Line Chart
                if not df.empty and 'altitude' in df.columns and 'heading' in df.columns:
                    st.line_chart(df[['altitude', 'heading']])  # Adjust columns as needed

                # Area Chart
                if 'weather' in data and 'temperature' in data['weather']:
                    df_weather = pd.DataFrame(data['weather'])
                    st.area_chart(df_weather[['temperature', 'wind_speed']])  # Adjust columns as needed

    elif option == "Airports":
        st.header("Airports")
        icao = st.text_input("Enter ICAO Code (e.g., KMIA)")
        if st.button("Fetch Airport Data"):
            data = fetch_data("airports", {"apt": icao})
            if data:
                # Debugging: Inspect the data
                st.write("Airport data:", data)

                try:
                    # Convert latitude and longitude to decimal format
                    lat_deg, lat_min = data['latitude'].split('-')[:2]
                    lon_deg, lon_min = data['longitude'].split('-')[:2]
                    latitude = convert_to_decimal(lat_deg, lat_min, data['latitude'][-1])
                    longitude = convert_to_decimal(lon_deg, lon_min, data['longitude'][-1])

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
                    
                    df = pd.DataFrame([data])
                    st.dataframe(df)
                except KeyError as e:
                    st.error(f"Key error: {e}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    elif option == "Preferred Routes":
        st.header("Preferred Routes")
        departure = st.text_input("Enter Departure ICAO (e.g., KATL)")
        arrival = st.text_input("Enter Arrival ICAO (e.g., KDFW)")
        if st.button("Fetch Preferred Routes"):
            data = fetch_data("preferred-routes", {"dep": departure, "arr": arrival})
            if data:
                # Debugging: Inspect the data
                st.write("Preferred routes data:", data)

                df = pd.DataFrame(data)
                st.dataframe(df)

                # Bar Chart
                if not df.empty and 'route_id' in df.columns and 'distance' in df.columns:
                    st.bar_chart(df.set_index('route_id')['distance'])

    elif option == "Weather METAR":
        st.header("Weather METAR")
        icao = st.text_input("Enter ICAO Code (e.g., KAVL)")
        if st.button("Fetch METAR"):
            data = fetch_data("weather/metar", {"apt": icao})
            if data:
                # Debugging: Inspect the data
                st.write("METAR data:", data)

                st.json(data)

                # Line Chart for METAR data
                if 'temperature' in data:
                    df_temp = pd.DataFrame(data['temperature'])
                    st.line_chart(df_temp[['temperature']])

    elif option == "Weather TAF":
        st.header("Weather TAF")
        icao = st.text_input("Enter ICAO Code (e.g., KAVL)")
        if st.button("Fetch TAF"):
            data = fetch_data("weather/taf", {"apt": icao})
            if data:
                # Debugging: Inspect the data
                st.write("TAF data:", data)

                st.json(data)

                # Area Chart for TAF data
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
                # Debugging: Inspect the data
                st.write("VATSIM pilots data:", data)

                df = pd.DataFrame(data)
                st.dataframe(df)

                # Map for VATSIM Pilots
                if 'lat' in df.columns and 'lon' in df.columns:
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
                else:
                    st.error("Latitude or longitude columns not found in VATSIM pilots data.")

    elif option == "VATSIM Controllers":
        st.header("VATSIM Controllers")
        facility = st.text_input("Enter Facility (e.g., CLT)")
        if st.button("Fetch VATSIM Controllers"):
            data = fetch_data("vatsim/controllers", {"fac": facility})
            if data:
                # Debugging: Inspect the data
                st.write("VATSIM controllers data:", data)

                df = pd.DataFrame(data)
                st.dataframe(df)
                st.success("VATSIM controllers data fetched successfully!")

if __name__ == "__main__":
    main()
