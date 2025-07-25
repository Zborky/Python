import googlemaps
import pandas as pd
import os

# Step 1: Initialization
def initialize_gmaps(api_key):
    """Initializes the Google Maps client with the provided API key."""
    return googlemaps.Client(key=api_key)

# Step 2: Define functions
def get_distance_and_duration(gmaps, city1, city2):
    """Gets the driving distance and travel time between two cities using Google Maps API."""
    try:
        result = gmaps.distance_matrix(origins=city1, destinations=city2, mode='driving')
        if result['status'] == 'OK':
            distance = result['rows'][0]['elements'][0]['distance']['text']
            duration = result['rows'][0]['elements'][0]['duration']['text']
            return distance, duration
        else:
            print(f"Failed to retrieve data for cities: {city1} and {city2}")
            return None, None
    except Exception as e:
        print(f"Error while fetching data between cities {city1} and {city2}: {e}")
        return None, None

def get_postal_code(gmaps, city):
    """Gets the postal code of a city using Google Maps Geocoding API."""
    try:
        geocode_result = gmaps.geocode(city)
        if geocode_result:
            for component in geocode_result[0]['address_components']:
                if 'postal_code' in component['types']:
                    return component['long_name']
        print(f"Failed to retrieve postal code for city: {city}")
        return None
    except Exception as e:
        print(f"Error while fetching postal code for city {city}: {e}")
        return None

def load_excel_file(input_file_path):
    """Loads data from an Excel file."""
    if not os.path.exists(input_file_path):
        print(f"Error: File {input_file_path} does not exist.")
        return None
    return pd.read_excel(input_file_path)

def save_to_excel(df, output_file_path):
    """Saves a DataFrame to an Excel file."""
    df.to_excel(output_file_path, index=False)
    print(f"Processing completed. Results saved to {output_file_path}")

# Step 3: Load data and process distances
def process_distances_and_durations(input_file_path, output_file_path, api_key):
    gmaps = initialize_gmaps(api_key)
    df = load_excel_file(input_file_path)
    if df is not None:
        # Add new columns to the DataFrame
        df['Vzdialenosť autom (km)'] = None  # Driving distance
        df['Čas cesty (min)'] = None          # Travel time
        df['PSČ Mesto1'] = None               # Postal code of City 1
        df['PSČ Mesto2'] = None               # Postal code of City 2
        for index, row in df.iterrows():
            city1 = row['Mesto1']
            city2 = row['Mesto2']
            print(f"Processing pair: {city1} - {city2}")
            # Get distance and duration
            distance, duration = get_distance_and_duration(gmaps, city1, city2)
            # Get postal codes for both cities
            postal_code1 = get_postal_code(gmaps, city1)
            postal_code2 = get_postal_code(gmaps, city2)
            
            # Save results into the DataFrame
            if distance and duration:
                df.at[index, 'Vzdialenosť autom (km)'] = distance
                df.at[index, 'Čas cesty (min)'] = duration
                df.at[index, 'PSČ Mesto1'] = postal_code1
                df.at[index, 'PSČ Mesto2'] = postal_code2
                print(f"Distance: {distance}, Duration: {duration}, Postal Code City1: {postal_code1}, Postal Code City2: {postal_code2}\n")
            else:
                print(f"Unable to retrieve data for cities {city1} and {city2}.")
        save_to_excel(df, output_file_path)

# Step 4: Define file paths and run the process
input_file_path = "C:/Users/Jakub/Desktop/Programovanie/Python/Distance/nazvy_miest.xlsx"
output_file_path = "C:/Users/Jakub/Desktop/Programovanie/Python/Distance/nazvy_miest_s_vzdialenostami_a_casom.xlsx"
api_key = "AIzaSyApPAjyICkSHcF4q_sfJlw3kLKrlCLULBQ"

# Start the processing
process_distances_and_durations(input_file_path, output_file_path, api_key)
