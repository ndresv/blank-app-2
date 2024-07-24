import streamlit as st
import requests

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
                st.json(data)
    
    elif option == "Preferred Routes":
        st.header("Preferred Routes")
        departure = st.text_input("Enter Departure ICAO (e.g., KATL)")
        arrival = st.text_input("Enter Arrival ICAO (e.g., KDFW)")
        if st.button("Fetch Preferred Routes"):
            data = fetch_data("preferred-routes", {"dep": departure, "arr": arrival})
            if data:
                st.json(data)
    
    elif option == "Weather METAR":
        st.header("Weather METAR")
        icao = st.text_input("Enter ICAO Code (e.g., KAVL)")
        if st.button("Fetch METAR"):
            data = fetch_data("weather/metar", {"apt": icao})
            if data:
                st.json(data)
    
    elif option == "Weather TAF":
        st.header("Weather TAF")
        icao = st.text_input("Enter ICAO Code (e.g., KAVL)")
        if st.button("Fetch TAF"):
            data = fetch_data("weather/taf", {"apt": icao})
            if data:
                st.json(data)
    
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
                st.json(data)
    
    elif option == "VATSIM Controllers":
        st.header("VATSIM Controllers")
        facility = st.text_input("Enter Facility (e.g., CLT)")
        if st.button("Fetch VATSIM Controllers"):
            data = fetch_data("vatsim/controllers", {"fac": facility})
            if data:
                st.json(data)

if __name__ == "__main__":
    main()
