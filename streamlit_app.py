import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import pydeck as pdk

# Set up the page layout
st.set_page_config(page_title="Football Stats", layout="wide")

# Sidebar configuration
st.sidebar.title("Football Stats Web App")
st.sidebar.markdown("Select options to filter data")

# API Request to fetch football data
api_key = "EuO4CTVqJ9exA0Oe04kE6BYAlCMmESs468pYDGbg1m7sl80fvwrncVSubpQB"
base_url = "https://api.sportmonks.com/v3/football/"

def get_data(endpoint, params=None):
    url = f"{base_url}{endpoint}"
    params = params or {}
    params["api_token"] = api_key
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data from {endpoint}. Error: {response.json()['error']['message']}")
        return None

# Fetch data
teams = get_data("teams")
fixtures = get_data("fixtures")
standings = get_data("standings")
players = get_data("players")

# Check if data fetching was successful
if teams and fixtures and standings and players:
    # Convert data to DataFrame
    teams_df = pd.json_normalize(teams['data']) if 'data' in teams else pd.DataFrame()
    fixtures_df = pd.json_normalize(fixtures['data']) if 'data' in fixtures else pd.DataFrame()
    standings_df = pd.json_normalize(standings['data']) if 'data' in standings else pd.DataFrame()
    players_df = pd.json_normalize(players['data']) if 'data' in players else pd.DataFrame()

    # Select box for teams
    team_names = teams_df['name'].tolist()
    selected_team = st.sidebar.selectbox("Select a Team", team_names)

    # Filter fixtures by selected team
    filtered_fixtures = fixtures_df[fixtures_df['localTeam.name'] == selected_team]

    # Display team fixtures
    st.header(f"Fixtures for {selected_team}")
    st.dataframe(filtered_fixtures[['date', 'localTeam.name', 'visitorTeam.name', 'status']])

    # Line chart for team performance
    st.header(f"{selected_team} Performance Over Time")
    fig, ax = plt.subplots()
    ax.plot(filtered_fixtures['date'], filtered_fixtures['scores.localteam_score'], label="Local Team Score")
    ax.plot(filtered_fixtures['date'], filtered_fixtures['scores.visitorteam_score'], label="Visitor Team Score")
    ax.set_xlabel("Date")
    ax.set_ylabel("Score")
    ax.legend()
    st.pyplot(fig)

    # Bar chart for standings
    st.header("League Standings")
    st.bar_chart(standings_df[['team_id', 'points']])

    # Map of stadiums
    st.header("Stadium Locations")
    stadium_locations = teams_df[['name', 'venue.latitude', 'venue.longitude']].dropna()
    stadium_locations.columns = ['name', 'lat', 'lon']
    st.map(stadium_locations)

    # Interactive Widgets
    st.sidebar.header("User Interaction")
    if st.sidebar.button("Refresh Data"):
        st.experimental_rerun()

    show_standings = st.sidebar.checkbox("Show Standings")
    if show_standings:
        st.success("Standings are displayed in the bar chart above")

    # Additional Widgets
    st.sidebar.text_input("Search for a player", key="search_player")
    st.sidebar.slider("Filter by Age", 15, 40, (20, 30))
    st.sidebar.color_picker("Pick a Theme Color")

    # Conclusion
    st.sidebar.info("Football Stats Web App provides an interactive platform to view football data and stats.")

    # Final output
    st.write("Developed by [Your Name]. Data provided by Sportmonks Football API.")
else:
    st.error("Failed to fetch required data. Please check the API endpoints and your API key.")
