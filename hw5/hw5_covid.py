# Import necessary libraries
import requests  # For making HTTP requests
import json  # For handling JSON data
import os  # For file and directory operations
from statistics import mean  # For calculating averages
from datetime import datetime  # For date manipulations
from collections import defaultdict  # For counting cases per month

def read_state_codes(filename):
    """
    Read state codes from a file.
    
    :param filename: Path to the file containing state codes
    :return: List of state codes
    """
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

# Read state codes from the file
state_codes = read_state_codes('hw5\state_territories.txt')

def fetch_and_save_state_data(state_code):
    """
    Fetch COVID-19 data for a given state and save it as a JSON file.
    
    :param state_code: Two-letter state code
    :return: Dictionary containing the state's COVID-19 data, or None if fetch fails
    """
    url = f"https://api.covidtracking.com/v1/states/{state_code.lower()}/daily.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Save JSON data to a file in the hw5 folder
        hw5 = 'hw5'  # Define the hw5 variable with the correct path
        file_path = os.path.join(hw5, f"{state_code.lower()}.json")
        with open(file_path, "w") as f:
            json.dump(data, f)
        
        return data
    else:
        print(f"Failed to fetch data for {state_code}")
        return None

def analyze_state_data(state_code, data_dict):
    """
    Analyze COVID-19 data for a given state and print statistics.
    
    :param state_code: Two-letter state code
    :param data_dict: Dictionary containing the state's COVID-19 data
    """
    if not data_dict:
        return
    
    # Extract positive increases (new cases) for each day
    positive_increases = [day['positiveIncrease'] for day in data_dict if 'positiveIncrease' in day]
    
    # Calculate average daily cases
    avg_daily_cases = mean(positive_increases)
    
    # Find the day with the highest number of new cases
    highest_day = max(data_dict, key=lambda x: x.get('positiveIncrease', 0))
    highest_date = datetime.strptime(str(highest_day['date']), "%Y%m%d").strftime("%Y-%m-%d")
    
    # Find the most recent date with no new cases
    no_new_cases = [day for day in data_dict if day.get('positiveIncrease', 0) == 0]
    most_recent_no_cases = min(no_new_cases, key=lambda x: x['date'])['date'] if no_new_cases else "N/A"
    most_recent_no_cases = datetime.strptime(str(most_recent_no_cases), "%Y%m%d").strftime("%Y-%m-%d") if most_recent_no_cases != "N/A" else "N/A"
    
    # Calculate total cases for each month
    monthly_cases = defaultdict(int)
    for day in data_dict:
        month = datetime.strptime(str(day['date']), "%Y%m%d").strftime("%Y-%m")
        monthly_cases[month] += day.get('positiveIncrease', 0)
    
    # Find months with highest and lowest new cases
    highest_month = max(monthly_cases, key=monthly_cases.get)
    lowest_month = min(monthly_cases, key=monthly_cases.get)
    
    # Print the analysis results
    print("Covid confirmed cases statistics")
    print(f"State name: {state_code}")
    print(f"Average number of new daily confirmed cases for the entire state dataset: {avg_daily_cases:.2f}")
    print(f"Date with the highest new number of covid cases: {highest_date}")
    print(f"Most recent date with no new covid cases: {most_recent_no_cases}")
    print(f"Month with the highest new number of covid cases: {highest_month}")
    print(f"Month with the lowest new number of covid cases: {lowest_month}")
    print()  # Add a blank line between states

def main():
    """
    Main function to process data for all states.
    """
    for state in state_codes:
        data = fetch_and_save_state_data(state)
        analyze_state_data(state, data)

if __name__ == "__main__":
    main()