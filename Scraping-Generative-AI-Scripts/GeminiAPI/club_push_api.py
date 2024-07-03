import requests
import json
import time
import logging
import os
import csv
import subprocess
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read('app.config')
API_KEY = config.get('API', 'API_KEY_ARYAN')
ADD_CLUB_URL = config.get('URL', 'ADD_CLUB_URL')

# Define the URL and API key of [ from api.keys ]
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

# Define the headers
headers = {
    "Content-Type": "application/json",
}

logging.basicConfig(filename='running_clubs.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

dir_name = "club_data_json"
os.makedirs(dir_name, exist_ok=True)

# Specify the maximum number of API calls per run
max_api_calls = 1000

# Read the list of cities from the CSV file
cities = []
with open('cities_500.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cities.append(row['city'])

# Initialize counters for API calls
api_calls = 0

# Function to make API request and save response for a city
def fetch_running_clubs(city, api_calls):
    max_retries = 2
    attempt = 0
    
    file_name = os.path.join(dir_name, f"{city.replace(' ', '_').lower()}_running_clubs.json")
    
    # Check if the file already exists
    if os.path.exists(file_name):
        log_message = f"File for {city} already exists. Skipping API call."
        print(log_message)
        logging.info(log_message)
        return api_calls, False  # Return current api_calls count and False to indicate API call was skipped

    while attempt < max_retries:
        attempt += 1
        
        try:
            # Define the JSON request body
            data = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": f"Give me exhaustive list of running clubs in {city} in json format only. "
                                        f"name, link, social link, address, town, state, contactAddressStreet1, "
                                        f"contactAddressStreet2, contactAddressZip, insta, twitter, meetup link. put null if not found"
                            }
                        ]
                    }
                ]
            }

            # Send the POST request
            response = requests.post(url, headers=headers, json=data)

            # Check if the request was successful
            if response.status_code == 200:
                response_json = response.json()
                # Extract the content part from the response
                content = response_json["candidates"][0]["content"]["parts"][0]["text"]

                # Parse the extracted content as JSON
                running_clubs = json.loads(content.strip("```json\n").strip("\n```"))

                # Write the parsed JSON to a file
                with open(file_name, "w") as json_file:
                    json.dump(running_clubs, json_file, indent=4)
                
                log_message = f"Running clubs data for {city} has been saved to {file_name}"
                print(log_message)
                logging.info(log_message)
                
                # Send the running clubs data to the specified API
                send_running_clubs_to_api(running_clubs)
                
                return api_calls, True  # Return incremented api_calls count and True to indicate API call was successful
            else:
                log_message = f"Request for {city} failed with status code: {response.status_code}, Response: {response.text}"
                print(log_message)
                logging.error(log_message)
        except json.JSONDecodeError as e:
            log_message = f"Attempt {attempt} for {city} failed with JSONDecodeError: {e}"
            print(log_message)
            logging.error(log_message)
            if attempt < max_retries:
                print("Retrying...")
                logging.info("Retrying...")
        except Exception as e:
            log_message = f"Attempt {attempt} for {city} failed with error: {e}"
            print(log_message)
            logging.error(log_message)
            if attempt < max_retries:
                print("Retrying...")
                logging.info("Retrying...")

    return api_calls, False

def send_running_clubs_to_api(running_clubs):
    for club in running_clubs:
        name = club.get('name', '')
        website = club.get('link', '')
        address = club.get('address', '')
        city = club.get('town', '')
        state = club.get('state', '')
        fb = club.get('social link', '')
        contactAddressStreet1 = club.get('contactAddressStreet1', '')
        contactAddressStreet2 = club.get('contactAddressStreet2', '')
        contactAddressZip = club.get('contactAddressZip', '')
        insta = club.get('insta', '')
        twitter = club.get('twitter', '')
        meetup = club.get('meetup link', '')
        
        command = [
            'curl', '--location', f'{ADD_CLUB_URL}',
            '--header', 'accept: */*',
            '--header', 'accept-language: en-US,en;q=0.9',
            '--form', f'isRunningClub=true',
            '--form', f'isRunningCoach=false',
            '--form', f'name={name}',
            '--form', f'website={website}',
            '--form', f'contactAddressStreet1={contactAddressStreet1}',
            '--form', f'contactAddressStreet2={contactAddressStreet2}',
            '--form', f'contactAddressCity={city}',
            '--form', f'contactAddressState={state}',
            '--form', f'contactAddressZip={contactAddressZip}',
            '--form', f'fb={fb}',
            '--form', f'insta={insta}',
            '--form', f'twitter={twitter}',
            '--form', f'meetup={meetup}',
            '--form', f'isRunningStore=false',
            '--form', f'runs=[]',
            '--form', f'memberships=[]'
        ]
        
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            log_message = f"Successfully sent data for {name} to API"
            print(log_message)
            logging.info(log_message)
        else:
            log_message = f"Failed to send data for {name} to API. Error: {result.stderr}"
            print(log_message)
            logging.error(log_message)

start_time = time.time()

# Loop through the cities and fetch running clubs data for each
for city in cities:
    if api_calls >= max_api_calls:
        log_message = f"Maximum API calls limit of {max_api_calls} reached. Stopping for now."
        print(log_message)
        logging.info(log_message)
        break
    
    api_calls, api_call_made = fetch_running_clubs(city, api_calls)
    
    if api_call_made:
        # Increment the counter only if the API call was made
        api_calls += 1

total_time = time.time() - start_time

log_message = f"Total API calls made: {api_calls}. Total time taken: {total_time:.2f} seconds."
print(log_message)
logging.info(log_message)
