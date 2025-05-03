import requests
import json
from dotenv import load_dotenv
import os
import sys
from typing import Dict, Optional, Any, Union


import requests
from datetime import datetime

class SkyscannerFlightsAPI:
    def __init__(self, api_key, market='ES', locale='es-ES', currency='EUR'):
        """
        Initialize the Skyscanner Flights API client.

        Parameters:
        - api_key (str): Your Skyscanner API key.
        - market (str): Country code representing the user's market (e.g., 'ES' for Spain).
        - locale (str): Locale code for language and regional formatting (e.g., 'es-ES').
        - currency (str): Currency code for displaying prices (e.g., 'EUR').
        """
        self.api_key = api_key
        self.market = market
        self.locale = locale
        self.currency = currency
        self.headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }
        self.endpoint = 'https://partners.api.skyscanner.net/apiservices/v3/flights/indicative/search'

    def _build_query_leg(self, origin, destination=None, date_type='fixedDate', date_value=None):
        """
        Construct a query leg for the API request.

        Parameters:
        - origin (str): IATA code of the departure airport (e.g., 'BCN').
        - destination (str, optional): IATA code of the arrival airport (e.g., 'CDG'). If None, searches to anywhere.
        - date_type (str): Type of date specification ('fixedDate', 'dateRange', or 'anytime').
        - date_value (str or tuple): Date information corresponding to the date_type.

        Returns:
        - dict: A query leg dictionary for the API request.
        """
        origin_place = {"queryPlace": {"iata": origin}}
        destination_place = {"anywhere": True} if not destination else {"queryPlace": {"iata": destination}}

        if date_type == 'fixedDate':
            year, month, day = map(int, date_value.split('-'))
            date_info = {"fixedDate": {"year": year, "month": month, "day": day}}
        elif date_type == 'dateRange':
            start_date, end_date = date_value
            start_year, start_month, start_day = map(int, start_date.split('-'))
            end_year, end_month, end_day = map(int, end_date.split('-'))
            date_info = {
                "dateRange": {
                    "startDate": {"year": start_year, "month": start_month, "day": start_day},
                    "endDate": {"year": end_year, "month": end_month, "day": end_day}
                }
            }
        elif date_type == 'anytime':
            date_info = {"anytime": True}
        else:
            raise ValueError("Invalid date_type. Choose from 'fixedDate', 'dateRange', or 'anytime'.")

        return {
            "originPlace": origin_place,
            "destinationPlace": destination_place,
            **date_info
        }

    def _search(self, query_legs, date_grouping=None):
        """
        Perform the API search request.

        Parameters:
        - query_legs (list): List of query legs for the search.
        - date_grouping (str, optional): Date grouping type ('DATE_TIME_GROUPING_TYPE_BY_DATE', 'DATE_TIME_GROUPING_TYPE_BY_MONTH').

        Returns:
        - dict: Parsed JSON response containing flight price information.
        """
        payload = {
            "query": {
                "market": self.market,
                "locale": self.locale,
                "currency": self.currency,
                "queryLegs": query_legs
            }
        }
        if date_grouping:
            payload["query"]["dateTimeGroupingType"] = date_grouping

        response = requests.post(self.endpoint, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def search_flights(self, origin, destination, outbound_date, inbound_date=None):
        """
        Search for flights with specified origin, destination, and dates.

        Parameters:
        - origin (str): IATA code of the departure airport.
        - destination (str): IATA code of the arrival airport.
        - outbound_date (str): Departure date in 'YYYY-MM-DD' format.
        - inbound_date (str, optional): Return date in 'YYYY-MM-DD' format.

        Returns:
        - dict: Flight search results.
        """
        query_legs = [self._build_query_leg(origin, destination, 'fixedDate', outbound_date)]
        if inbound_date:
            query_legs.append(self._build_query_leg(destination, origin, 'fixedDate', inbound_date))
        return self._search(query_legs)

    def search_flights_flexible_dates(self, origin, destination, start_date, end_date, grouping='DATE_TIME_GROUPING_TYPE_BY_DATE'):
        """
        Search for flights with specified origin and destination over a date range.

        Parameters:
        - origin (str): IATA code of the departure airport.
        - destination (str): IATA code of the arrival airport.
        - start_date (str): Start date in 'YYYY-MM-DD' format.
        - end_date (str): End date in 'YYYY-MM-DD' format.
        - grouping (str): Date grouping type.

        Returns:
        - dict: Flight search results.
        """
        query_leg = self._build_query_leg(origin, destination, 'dateRange', (start_date, end_date))
        return self._search([query_leg], date_grouping=grouping)

    def search_flights_to_anywhere(self, origin, date=None, date_type='fixedDate'):
        """
        Search for flights from a specified origin to anywhere.

        Parameters:
        - origin (str): IATA code of the departure airport.
        - date (str or tuple, optional): Date information corresponding to the date_type.
        - date_type (str): Type of date specification.

        Returns:
        - dict: Flight search results.
        """
        query_leg = self._build_query_leg(origin, None, date_type, date)
        return self._search([query_leg])

    def search_flights_anytime(self, origin, destination):
        """
        Search for flights with specified origin and destination at any time.

        Parameters:
        - origin (str): IATA code of the departure airport.
        - destination (str): IATA code of the arrival airport.

        Returns:
        - dict: Flight search results.
        """
        query_leg = self._build_query_leg(origin, destination, 'anytime')
        return self._search([query_leg], date_grouping='DATE_TIME_GROUPING_TYPE_BY_MONTH')




def main() -> None:
    """
    Main function to execute the flight search and print results with examples of different API calls.
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Access environment variables
    api_key = os.getenv("SKYSCANNER_API_KEY")
    if not api_key:
        print("Error: SKYSCANNER_API_KEY environment variable not found.")
        return None
    
    client = SkyscannerFlightsAPI(api_key=api_key)
    
    # Example 1: Basic one-way flight search
    print("\n=== Example 1: Basic one-way flight search ===")
    results = client.search_flights(
        origin="BCN",  # Barcelona
        destination="LHR",  # London Heathrow
        outbound_date="2025-06-15"
    )
    print_results(results, "Basic one-way flight search")
    
    # Example 2: Round-trip flight search
    print("\n=== Example 2: Round-trip flight search ===")
    results = client.search_flights(
        origin="BCN",  # Barcelona
        destination="CDG",  # Paris Charles de Gaulle
        outbound_date="2025-07-10",
        inbound_date="2025-07-17"
    )
    print_results(results, "Round-trip flight search")
    
    # Example 3: Flexible dates search
    print("\n=== Example 3: Flexible dates search ===")
    results = client.search_flights_flexible_dates(
        origin="BCN",  # Barcelona
        destination="AMS",  # Amsterdam
        start_date="2025-08-01",
        end_date="2025-08-31"
    )
    print_results(results, "Flexible dates search")
    
    # Example 4: Flights to anywhere search
    print("\n=== Example 4: Flights to anywhere search ===")
    results = client.search_flights_to_anywhere(
        origin="BCN",  # Barcelona
        date="2025-09-15",
        date_type="fixedDate"
    )
    print_results(results, "Flights to anywhere search")
    
    # Example 5: Anytime flights search
    print("\n=== Example 5: Anytime flights search ===")
    results = client.search_flights_anytime(
        origin="BCN",  # Barcelona
        destination="JFK"  # New York
    )
    print_results(results, "Anytime flights search")
    
    return None


def print_results(results, search_type):
    """
    Saves flight search results to a JSON file without console output.
    
    Parameters:
    - results (dict): The flight search results from Skyscanner API
    - search_type (str): Description of the search type for the filename
    """
    # Create timestamp for unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create filename with search type and timestamp
    filename = f"flight_results_{search_type.replace(' ', '_')}_{timestamp}.json"
    
    # Save results to JSON file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    # No console output as requested

# Example usage
if __name__ == "__main__":
    main()