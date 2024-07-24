import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pydeck as pdk

# API URLs
AIRPORTS_API_URL = "https://api.aviationapi.com/v1/airports"
WEATHER_METAR_API_URL = "https://api.aviationapi.com/v1/weather/metar"
VATSIM_PILOTS_API_URL = "https://api.aviationapi.com/v1/vatsim/pilots"

# Function to fetch data from APIs
def fetch_data(api_url, params=None):
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching data: {response.status_code} - {response.text}")
        return None

# Sidebar options
st.sidebar.header("Options")
api_choice = st.sidebar.selectbox("Choose API", ["Airports", "Weather METAR", "VATSIM Pilots"])
airport_code = st.sidebar.text_input("Enter ICAO Airport Code (e.g., KMIA)", "KMIA")

if api_choice == "Airports":
    if airport_code:
        st.sidebar.button("Get Airport Data")
        data = fetch_data(AIRPORTS_API_URL, params={"apt": airport_code})
        if data:
            st.write(f"### Airport Data for {airport_code}")
            st.dataframe(pd.DataFrame([data]))

            # Map of the airport
            st.write("### Map of the Selected Airport")
            location = {"lat": data["latitude"], "lon": data["longitude"]}
            map_data = pd.DataFrame([location])
            st.pydeck_chart(pdk.Deck(
                initial_view_state=pdk.ViewState(
                    latitude=location["lat"],
                    longitude=location["lon"],
                    zoom=10
                ),
                layers=[
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=map_data,
                        get_position="[lon, lat]",
                        auto_highlight=True,
                        radius_scale=6,
                        radius_min_pixels=1,
                        radius_max_pixels=100,
                        line_width_min_pixels=1,
                        get_fill_color="[200, 30, 0, 160]",
                        get_line_color="[0, 0, 0, 255]"
                    )
                ]
            ))

elif api_choice == "Weather METAR":
    if airport_code:
        st.sidebar.button("Get Weather Data")
        data = fetch_data(WEATHER_METAR_API_URL, params={"apt": airport_code})
        if data:
            st.write(f"### METAR Data for {airport_code}")
            st.dataframe(pd.DataFrame([data]))

            # Line chart for temperature
            st.write("### Temperature Over Time")
            dates = pd.to_datetime([data["time_of_obs"]])
            temperatures = [float(data["temp"])]
            temp_df = pd.DataFrame({"Date": dates, "Temperature": temperatures})
            st.line_chart(temp_df.set_index("Date"))

            # Area chart for visibility
            st.write("### Visibility Over Time")
            visibilities = [float(data["visibility"])]
            visibility_df = pd.DataFrame({"Date": dates, "Visibility": visibilities})
            st.area_chart(visibility_df.set_index("Date"))

elif api_choice == "VATSIM Pilots":
    if airport_code:
        st.sidebar.button("Get VATSIM Data")
        data = fetch_data(VATSIM_PILOTS_API_URL, params={"apt": airport_code})
        if data:
            st.write(f"### VATSIM Pilots Data for {airport_code}")
            st.dataframe(pd.DataFrame(data))

            # Bar chart for number of pilots
            st.write("### Number of Pilots by Aircraft Type")
            aircraft_types = pd.Series([d["aircraft"] for d in data]).value_counts()
            st.bar_chart(aircraft_types)

            # Map of pilots
            st.write("### Map of Pilots' Locations")
            pilots_data = pd.DataFrame([
                {"lat": float(p["latitude"]), "lon": float(p["longitude"])}
                for p in data if p["latitude"] and p["longitude"]
            ])
            st.pydeck_chart(pdk.Deck(
                initial_view_state=pdk.ViewState(
                    latitude=pilots_data["lat"].mean(),
                    longitude=pilots_data["lon"].mean(),
                    zoom=5
                ),
                layers=[
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=pilots_data,
                        get_position="[lon, lat]",
                        auto_highlight=True,
                        radius_scale=6,
                        radius_min_pixels=1,
                        radius_max_pixels=100,
                        line_width_min_pixels=1,
                        get_fill_color="[0, 200, 30, 160]",
                        get_line_color="[0, 0, 0, 255]"
                    )
                ]
            ))

# Additional Widgets
st.sidebar.write("### Additional Widgets")
if st.sidebar.checkbox("Show Airport Data", value=True):
    st.sidebar.selectbox("Select Metric", ["Flights", "Weather", "Traffic"])

# Feedback Boxes
if api_choice == "Airports" and data:
    st.success("Successfully fetched airport data!")
elif api_choice == "Weather METAR" and data:
    st.info("Weather data retrieved successfully.")
elif api_choice == "VATSIM Pilots" and data:
    st.warning("VATSIM data loaded. Check map and table for details.")
else:
    st.error("No data available. Please check the API and try again.")
