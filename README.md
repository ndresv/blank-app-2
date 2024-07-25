# Aviation Data Explorer

## Overview
The **Aviation Data Explorer** is a web application developed using Streamlit. It allows users to fetch and visualize aviation data from various APIs, including information about airports, preferred routes, VATSIM pilots, and charts. The application features interactive tables, charts, and maps to enhance data exploration and analysis.

## Features Implemented
The application incorporates the following features:

1. **API Requests**: Fetch data from selected APIs.
2. **Interactive Tables**: Display data in a tabular format.
3. **Chart Elements**: Include line, area, and bar charts.
4. **Map Visualization**: Display maps with points marked on them.
5. **Widgets**:
   - Button
   - Checkbox
   - Radio button
   - Selectbox
   - Slider
   - Text input
6. **Feedback and Messages**:
   - Success box
   - Warning box
   - Error box

## Sidebar Options
The sidebar contains options for selecting different APIs and their corresponding functionalities:

### 1. **Airports**
   - **ICAO Code**: Enter the ICAO code of the airport (e.g., KMIA).
   - **Fetch Airport Data**: Button to fetch and display airport data.
   - **Enable Map View**: Checkbox to enable or disable map view for the selected airport.
   - **Comparison**: Option to enter a second ICAO code for comparing two airports.

### 2. **Preferred Routes**
   - **Fetch Preferred Routes Data**: Button to fetch and display preferred routes data.

### 3. **VATSIM Pilots**
   - **ICAO Code**: Enter the ICAO code to fetch VATSIM pilots data.
   - **Fetch VATSIM Pilots Data**: Button to fetch and display VATSIM pilots data.

### 4. **Charts**
   - **ICAO Code**: Enter the ICAO code to fetch chart data.
   - **Chart Group**: Select the chart group (e.g., General, Departures, Arrivals, Approaches).
   - **Fetch Charts Data**: Button to fetch and display chart data.
