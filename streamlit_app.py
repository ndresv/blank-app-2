import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt

# Sample data for charts and tables
airport_data = {
    "site_number": ["16517.5*A"],
    "facility_name": ["ASHEVILLE RGNL"],
    "faa_ident": ["AVL"],
    "icao_ident": ["KAVL"],
    "state": ["NC"],
    "city": ["ASHEVILLE"],
    "elevation": [2162],
    "latitude": ["35-26-04.0000N"],
    "longitude": ["082-32-33.8240W"]
}

weather_data = {
    "station_id": ["KDVK"],
    "temp": [3.0],
    "dewpoint": [0.0],
    "wind": ["190"],
    "wind_vel": [8],
    "visibility": [10.0],
    "alt_hg": [29.89]
}

preferred_routes_data = {
    "origin": ["ABQ"],
    "route": ["ABQ DIESL TTORO3 IAH"],
    "destination": ["IAH"],
    "altitude": [350]
}

vatsim_data = {
    "callsign": ["AAL1567"],
    "latitude": [32.30375],
    "longitude": [-94.69470],
    "altitude": [35974],
    "ground_speed": [403]
}

# Convert to DataFrame
airport_df = pd.DataFrame(airport_data)
weather_df = pd.DataFrame(weather_data)
preferred_routes_df = pd.DataFrame(preferred_routes_data)
vatsim_df = pd.DataFrame(vatsim_data)

# Streamlit layout
st.title("FAA Aeronautical Charts and Publications")

# Sidebar
st.sidebar.header("Filter Options")

selected_option = st.sidebar.selectbox("Select Data", ["Airport Information", "Weather Data", "Preferred Routes", "VATSIM Data"])

if selected_option == "Airport Information":
    st.subheader("Airport Information")
    st.dataframe(airport_df)
    
    # Display a bar chart for airport elevation data
    st.subheader("Airport Elevation Chart")
    st.bar_chart(airport_df[['elevation']])

elif selected_option == "Weather Data":
    st.subheader("Weather Information")
    st.dataframe(weather_df)
    
    # Display line and area charts for weather data
    st.subheader("Weather Data Charts")
    st.line_chart(weather_df[['temp', 'dewpoint']])
    st.area_chart(weather_df[['visibility']])
    
    # Display a map with weather station
    st.subheader("Weather Station Map")
    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(latitude=32.30375, longitude=-94.69470, zoom=10),
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
    st.dataframe(preferred_routes_df)
    
    # Display a bar chart for preferred route altitude data
    st.subheader("Preferred Routes Altitude Chart")
    st.bar_chart(preferred_routes_df[['altitude']])

elif selected_option == "VATSIM Data":
    st.subheader("VATSIM Data")
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
st.warning("Ensure that API keys and endpoints are correctly configured.")
st.error("An error occurred while fetching data.")

# Additional Widgets
radio_option = st.radio("Choose an option", ["Option 1", "Option 2"])
text_input = st.text_input("Enter some text")

# Display widgets
st.write("Radio Option Selected:", radio_option)
st.write("Text Input:", text_input)
