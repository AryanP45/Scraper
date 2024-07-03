### README for Gemini and GPT API Scripts

This repository contains scripts to interact with Gemini and GPT APIs for fetching data related to running clubs, coaches, and shops across various cities. The directory is structured as follows:

```
.
├── cities_sorted_by_total_income.csv
├── GeminiAPI
│   ├── cities.csv
│   ├── club_data_json
│   ├── coaches_data_json
│   ├── gemini_api_scrapper.py
│   ├── gemini_fetch_running_clubs.py
│   ├── gemini_fetch_running_coaches.py
│   ├── gemini_fetch_running_shops.py
│   ├── running_clubs.log
│   ├── running_coaches.log
│   ├── running_shops.log
│   └── shop_data_json
├── GPT_API
│   ├── cities.csv
│   ├── club_data_json
│   ├── coaches_data_json
│   ├── gpt_fetch_running_clubs.py
│   ├── gpt_fetch_running_coaches.py
│   ├── gpt_fetch_running_shops.py
│   ├── running_clubs.log
│   ├── running_coaches.log
│   ├── running_shops.log
│   └── shop_data_json
├── Json_to_Excel
└── README.md
```

### Example: Fetching Running Clubs with Gemini API

#### Script: `gemini_fetch_running_clubs.py`

**Flow:**
1. **Initialization**:
   - Imports necessary libraries (`requests`, `json`, `time`, `logging`, `os`, `csv`).
   - Defines the API URL and headers.
   - Sets up logging and creates the output directory if it doesn't exist.

2. **Reading Cities**:
   - Reads a list of cities from `cities.csv`.

3. **API Calls**:
   - Iterates through each city.
   - For each city, it checks if the JSON file already exists in `club_data_json` directory.
   - If the file does not exist, it makes an API call to fetch the data.
   - The data is saved in a JSON file named after the city.

4. **Error Handling**:
   - Implements retries for API calls in case of errors.
   - Logs errors and successful operations.

5. **Completion**:
   - Logs the total number of API calls made and the total time taken for the script to run.

**Usage**:
- Place the cities to be queried in `GeminiAPI/cities.csv`.
- Run the script using `python gemini_fetch_running_clubs.py`.
- The fetched data will be stored in `GeminiAPI/club_data_json` directory.
- Check `running_clubs.log` for logs of the operations.

### Notes

- **API Keys**: Ensure the API Keys are valid and configured correctly in the scripts.
- **Log Files**: Check log files for details on operations and any errors encountered.
- **MAX_API_CALLS**: Use this variable carefully to limit api calls.
