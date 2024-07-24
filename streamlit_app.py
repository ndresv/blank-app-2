import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pydeck as pdk

# API endpoints
AVIATION_API_BASE = 'https://api.aviationapi.com/v1'
AIRPORTS_ENDPOINT = f'{AVIATION_API_BASE}/airports'
CHARTS_ENDPOINT = f'{AVIATION_API_BASE}/charts'
PREFERRED_ROUTES_ENDPOINT = f'{AVIATION_API_BASE}/preferred-routes'
WEATHER_METAR_ENDPOINT = f'{AVIATION_API_BASE}/weather/metar'
VATSIM_PILOTS_ENDPOINT = f'{AVIATION_API_BASE}/vatsim/pilots'
VATSIM_CONTROLLERS_ENDPOINT = f'{AVIATION_API_BASE}/vatsim/controllers'

# Sidebar for selection
st.sidebar.title("Aviation API Dashboard")
option = st.sidebar.selectbox("Select an option", ["Airport Data", "Charts", "Preferred Routes", "Weather METAR", "VATSIM Pilots", "VATSIM Controllers"])

if option == "Airport Data":
    icao_code = st.sidebar.text_input("Enter ICAO airport code (e.g., KATL)")
    if icao_code:
        st.sidebar.success("Fetching data...")
        airport_response = requests.get(f'{AIRPORTS_ENDPOINT}/{icao_code}')
        if airport_response.status_code == 200:
            airport_data = airport_response.json()
            st.title(f"Airport Information for {icao_code}")
            st.json(airport_data)
            
            # Display airport location on map
            st.subheader("Airport Location")
            st.map(pd.DataFrame({
                'lat': [airport_data['lat']],
                'lon': [airport_data['lon']]
            }, index=[icao_code]))
            
            # Fetch and display charts for selected airport
            charts_response = requests.get(f'{CHARTS_ENDPOINT}?apt={icao_code}')
            if charts_response.status_code == 200:
                charts_data = charts_response.json()
                st.subheader("Airport Charts")
                st.write(pd.DataFrame(charts_data))
            
            # Fetch and display METAR data
            metar_response = requests.get(f'{WEATHER_METAR_ENDPOINT}?apt={icao_code}')
            if metar_response.status_code == 200:
                metar_data = metar_response.json()
                st.subheader("METAR Data")
                st.json(metar_data)
        else:
            st.error(f"Airport data not found for {icao_code}")

elif option == "Charts":
    st.sidebar.success("Fetching charts...")
    charts_response = requests.get(CHARTS_ENDPOINT)
    if charts_response.status_code == 200:
        charts_data = charts_response.json()
        st.title("Charts Data")
        st.write(pd.DataFrame(charts_data))
    else:
        st.error("Failed to fetch charts data")

elif option == "Preferred Routes":
    st.sidebar.success("Fetching preferred routes...")
    routes_response = requests.get(PREFERRED_ROUTES_ENDPOINT)
    if routes_response.status_code == 200:
        routes_data = routes_response.json()
        st.title("Preferred Routes")
        st.write(pd.DataFrame(routes_data))
    else:
        st.error("Failed to fetch preferred routes")

elif option == "Weather METAR":
    icao_code = st.sidebar.text_input("Enter ICAO airport code (e.g., KAVL)")
    if icao_code:
        st.sidebar.success("Fetching METAR data...")
        metar_response = requests.get(f'{WEATHER_METAR_ENDPOINT}?apt={icao_code}')
        if metar_response.status_code == 200:
            metar_data = metar_response.json()
            st.title(f"METAR Data for {icao_code}")
            st.json(metar_data)
            
            # Display METAR data in line and area charts
            if 'temperature' in metar_data:
                temp_data = pd.DataFrame({
                    'Temperature': [metar_data['temp']]
                })
                st.subheader("Temperature Line Chart")
                st.line_chart(temp_data)
                
                st.subheader("Temperature Area Chart")
                st.area_chart(temp_data)
        else:
            st.error(f"METAR data not found for {icao_code}")

elif option == "VATSIM Pilots":
    airport_code = st.sidebar.text_input("Enter ICAO airport code for VATSIM pilots (e.g., KATL)")
    if airport_code:
        st.sidebar.success("Fetching VATSIM pilots data...")
        vatsim_response = requests.get(f'{VATSIM_PILOTS_ENDPOINT}?apt={airport_code}')
        if vatsim_response.status_code == 200:
            vatsim_data = vatsim_response.json()
            st.title(f"VATSIM Pilots at {airport_code}")
            st.write(pd.DataFrame(vatsim_data))
            
            # Display pilots on map
            st.subheader("VATSIM Pilots Location")
            pilots_df = pd.DataFrame({
                'lat': [pilot['latitude'] for pilot in vatsim_data],
                'lon': [pilot['longitude'] for pilot in vatsim_data]
            })
            st.pydeck_chart(pdk.Deck(
                initial_view_state=pdk.ViewState(latitude=pilots_df['lat'].mean(), longitude=pilots_df['lon'].mean(), zoom=5),
                layers=[pdk.Layer(
                    "ScatterplotLayer",
                    data=pilots_df,
                    get_position=["lon", "lat"],
                    auto_highlight=True,
                    radius_scale=10,
                    radius_min_pixels=5,
                    radius_max_pixels=100,
                    line_width_min_pixels=1,
                    get_fill_color=[255, 0, 0, 160],
                    get_line_color=[0, 0, 0, 200],
                    pickable=True
                )]
            ))
        else:
            st.error(f"VATSIM pilots data not found for {airport_code}")

elif option == "VATSIM Controllers":
    facility_code = st.sidebar.text_input("Enter facility code for VATSIM controllers (e.g., CHI)")
    if facility_code:
        st.sidebar.success("Fetching VATSIM controllers data...")
        vatsim_response = requests.get(f'{VATSIM_CONTROLLERS_ENDPOINT}?fac={facility_code}')
        if vatsim_response.status_code == 200:
            vatsim_data = vatsim_response.json()
            st.title(f"VATSIM Controllers at {facility_code}")
            st.write(pd.DataFrame(vatsim_data))
        else:
            st.error(f"VATSIM controllers data not found for {facility_code}")

# Add interactive elements
st.sidebar.subheader("Interactive Widgets")
if st.sidebar.button("Fetch Data"):
    st.sidebar.info("Fetching data based on selected options...")

show_warning = st.sidebar.checkbox("Show Warning", value=False)
if show_warning:
    st.sidebar.warning("This is a warning message.")

st.sidebar.radio("Select Display Option", ["Option 1", "Option 2"], index=0)
selected_option = st.sidebar.selectbox("Select Data Range", ["Last 24 Hours", "Last 7 Days", "Last 30 Days"])

number = st.sidebar.number_input("Input a number", min_value=1, max_value=100, value=50)
text = st.sidebar.text_area("Enter additional information", "Type here...")

# Progress bar
with st.sidebar.expander("Progress"):
    st.sidebar.progress(50)

# Media elements
st.image("https://via.placeholder.com/800x400", caption="Example Image")
