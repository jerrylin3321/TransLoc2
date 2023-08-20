# Bus Arrival Time Estimator

The Bus Arrival Time Estimator is a Python script that calculates the estimated time of arrival (ETA) for a bus given a departure location and an arrival location. The script leverages the Google Maps API for transit directions and integrates with the TransLoc API for real-time bus arrival information.

## Features

- **Calculate Arrival Time**: Computes the estimated arrival time for the bus including waiting time and travel time.
- **Flexible Input**: Takes departure and arrival locations as input and calculates the most suitable bus route.
- **Real-Time Data Integration**: Utilizes real-time data from the TransLoc API for accurate bus arrival predictions.

## Dependencies

- `requests`: For making HTTP requests to the TransLoc API.
- `googlemaps`: For fetching transit directions using the Google Maps API.
- `datetime`: For handling date and time calculations.
- `dateutil.parser`: For parsing date strings.

## Usage

1. **Set Up API Keys**: You'll need to set up API keys for both Google Maps and TransLoc APIs and replace them in the script where `API_KEY_HERE` is mentioned.

2. **Install Required Libraries**:

   ```bash
   pip install requests googlemaps python-dateutil
