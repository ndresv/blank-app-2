import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

# Base URL
BASE_URL = "https://api.aviationapi.com/v1"

# Helper function to fetch data from API
def fetch_data(endpoint, params={}):
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()  # Check for HTTP errors
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

# Streamlit App
def main():
    st.title("FAA Aeronautical Charts and Airport Information")

    # Sidebar for navigation
    st.sidebar.header("Navigation")
    option = st.sidebar.selectbox("Choose an option", 
                                  ["Charts", "Airports", "Preferred Routes", "Weather METAR", "Weather TAF", "VATSIM Pilots", "VATSIM Controllers"])

    if option in ["Charts", "Airports", "Preferred Routes", "Weather METAR", "Weather TAF", "VATSIM Pilots", "VATSIM Controllers"]:
        # Input for parameters
        st.sidebar.header("Parameters")
        if option in ["Airports", "Weather METAR", "Weather TAF"]:
            airport_code = st.sidebar.text_input("Enter Airport ICAO or FAA Code", "")
            if airport_code:
                params = {"id": airport_code} if option != "Preferred Routes" else {"search": airport_code}
            else:
                params = {}
        else:
            params = {}

        # Fetch and display data
        if option == "Charts":
            st.header("Charts")
            data = fetch_data("charts", params)
            if data:
                st.write(data)
                # Display data as interactive table
                df = pd.DataFrame(data)
                st.dataframe(df)

        elif option == "Airports":
            st.header("Airports")
            data = fetch_data("airports", params)
            if data:
                st.write(data)
                # Display data as interactive table
                df = pd.DataFrame(data)
                st.dataframe(df)

        elif option == "Preferred Routes":
            st.header("Preferred Routes")
            data = fetch_data("preferred-routes", params)
            if data:
                st.write(data)
                # Display data as interactive table
                df = pd.DataFrame(data)
                st.dataframe(df)

        elif option == "Weather METAR":
            st.header("Weather METAR")
            data = fetch_data("weather/metar", params)
            if data:
                st.write(data)
                # Display data as interactive table
                df = pd.DataFrame(data)
                st.dataframe(df)
                # Display a line chart for temperature if available
                if 'temp' in data[0]:
                    temperatures = [float(item['temp']) for item in data]
                    times = [datetime.datetime.now() for _ in data]
                    fig, ax = plt.subplots()
                    ax.plot(times, temperatures, label="Temperature")
                    ax.set_xlabel("Time")
                    ax.set_ylabel("Temperature (°C)")
                    ax.set_title("Temperature Over Time")
                    ax.xaxis.set_major_locator(mdates.HourLocator())
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
                    plt.xticks(rotation=45)
                    st.pyplot(fig)

        elif option == "Weather TAF":
            st.header("Weather TAF")
            data = fetch_data("weather/taf", params)
            if data:
                st.write(data)
                # Display data as interactive table
                df = pd.DataFrame(data)
                st.dataframe(df)

        elif option == "VATSIM Pilots":
            st.header("VATSIM Pilots")
            data = fetch_data("vatsim/pilots", params)
            if data:
                st.write(data)
                # Display data as interactive table
                df = pd.DataFrame(data)
                st.dataframe(df)

        elif option == "VATSIM Controllers":
            st.header("VATSIM Controllers")
            data = fetch_data("vatsim/controllers", params)
            if data:
                st.write(data)
                # Display data as interactive table
                df = pd.DataFrame(data)
                st.dataframe(df)

    # Add interactive widgets
    st.sidebar.header("Interactive Widgets")
    if st.sidebar.button('Show Info'):
        st.info("This is an information message")

    if st.sidebar.checkbox('Show Warning'):
        st.warning("This is a warning message")

    if st.sidebar.checkbox('Show Error'):
        st.error("This is an error message")

    if st.sidebar.radio('Select an Option', ['Option 1', 'Option 2']) == 'Option 1':
        st.success("You selected Option 1")

    st.sidebar.selectbox('Selectbox Example', ['Choice 1', 'Choice 2'])
    st.sidebar.slider('Slider Example', 0, 100, 50)
    st.sidebar.text_input('Text Input Example')
    st.sidebar.color_picker('Color Picker Example')

if __name__ == "__main__":
    main()
