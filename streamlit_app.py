import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

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
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return None

# Fetch data with nested includes for fixtures
fixtures_endpoint = "fixtures"
fixtures_params = {"include": "league;season;venue"}
fixtures = get_data(fixtures_endpoint, params=fixtures_params)

# Fetch leagues data
leagues = get_data("leagues")

# Check if data fetching was successful
if fixtures and leagues:
    # Convert data to DataFrame
    fixtures_df = pd.json_normalize(fixtures['data']) if 'data' in fixtures else pd.DataFrame()
    leagues_df = pd.json_normalize(leagues['data']) if 'data' in leagues else pd.DataFrame()

    st.write("Fixtures DataFrame Structure:")
    st.write(fixtures_df.head())

    st.write("Leagues DataFrame Structure:")
    st.write(leagues_df.head())

    # Display League Information
    st.header("Leagues Information")
    for _, league in leagues_df.iterrows():
        st.subheader(league['name'])
        st.image(league['image_path'], use_column_width=True)
        st.write(f"Short Code: {league['short_code']}")
        st.write(f"Country ID: {league['country_id']}")
        st.write(f"Last Played At: {league['last_played_at']}")
        st.write("------")

    # Select box for teams
    team_names = fixtures_df['name'].tolist()
    selected_team = st.sidebar.selectbox("Select a Team", team_names)

    # Filter fixtures by selected team
    filtered_fixtures = fixtures_df[
        (fixtures_df['name'].str.contains(selected_team, case=False))
    ]

    # Display team fixtures
    st.header(f"Fixtures for {selected_team}")
    st.dataframe(filtered_fixtures[['starting_at', 'name', 'result_info']])

    # Line chart for team performance (mock data since actual performance stats are missing)
    st.header(f"{selected_team} Performance Over Time")
    fig, ax = plt.subplots()
    # Assuming 'starting_at' is the date and mock scores
    filtered_fixtures['starting_at'] = pd.to_datetime(filtered_fixtures['starting_at'])
    filtered_fixtures['mock_score'] = [1, 2, 3, 4]  # Mock data
    ax.plot(filtered_fixtures['starting_at'], filtered_fixtures['mock_score'], label="Team Performance")
    ax.set_xlabel("Date")
    ax.set_ylabel("Performance")
    ax.legend()
    st.pyplot(fig)

    # Bar chart for standings
    st.header("League Standings")
    st.bar_chart(fixtures_df[['starting_at', 'result_info']])

    # Map of stadiums (mock data since actual lat/lon are missing)
    st.header("Stadium Locations")
    stadium_locations = fixtures_df[['name', 'venue.latitude', 'venue.longitude']].dropna()
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
