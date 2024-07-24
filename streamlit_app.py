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
    icao = st.sidebar.text_input("Enter ICAO Code (e.g., KATL)", value="KATL")
    date_filter = st.sidebar.date_input("Select date:", pd.to_datetime("today"))

    if option == "Charts":
        st.header("Charts")
        if st.button("Fetch Charts"):
            data = fetch_data("charts", {"apt": icao})
            if data:
                st.json(data)
                # Assuming data includes a structure for plotting
                if 'charts' in data:
                    charts_df = pd.DataFrame(data['charts'])
                    st.line_chart(charts_df[['altitude', 'heading']])  # Example line chart

    elif option == "Airports":
        st.header("Airports")
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
        if st.button("Fetch METAR"):
            data = fetch_data("weather/metar", {"apt": icao})
            if data:
                st.json(data)
                # Line chart example: Temperature over time
                metar_df = pd.DataFrame(data['data'])  # Adjust based on actual data structure
                st.line_chart(metar_df[['temp', 'wind_speed']])  # Example columns

    elif option == "Weather TAF":
        st.header("Weather TAF")
        if st.button("Fetch TAF"):
            data = fetch_data("weather/taf", {"apt": icao})
            if data:
                st.json(data)
                # Area chart example: Temperature trends
                taf_df = pd.DataFrame(data['data'])  # Adjust based on actual data structure
                st.area_chart(taf_df[['temp']])  # Example column

    elif option == "VATSIM Pilots":
        st.header("VATSIM Pilots")
        if st.button("Fetch VATSIM Pilots"):
            data = fetch_data("vatsim/pilots", {"apt": icao})
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df)  # Interactive table
                st.warning("VATSIM pilots data fetched successfully!")

    elif option == "VATSIM Controllers":
        st.header("VATSIM Controllers")
        if st.button("Fetch VATSIM Controllers"):
            data = fetch_data("vatsim/controllers", {"apt": icao})
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df)  # Interactive table
                st.success("VATSIM controllers data fetched successfully!")

    # Map Example
    st.header("Map with Points")
    points = {
        'lat': [37.7749, 34.0522, 40.7128],
        'lon': [-122.4194, -118.2437, -74.0060],
        'label': ['San Francisco', 'Los Angeles', 'New York']
    }
    df_points = pd.DataFrame(points)
    st.map(df_points)

    # Bar Chart Example
    st.header("Example Bar Chart")
    bar_data = {
        'City': ['San Francisco', 'Los Angeles', 'New York'],
        'Flights': [150, 200, 300]
    }
    df_bar = pd.DataFrame(bar_data)
    st.bar_chart(df_bar.set_index('City'))

    # Progress Bar Example
    st.header("Progress Bar Example")
    with st.spinner("Loading data..."):
        import time
        for i in range(100):
            time.sleep(0.05)
            st.progress(i + 1)

    # 3D Map Example
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
