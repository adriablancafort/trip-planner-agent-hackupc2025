import json
import os
from typing import Any, Dict, Optional
from datetime import datetime
from dotenv import load_dotenv
import requests

from typing import Optional, Dict, Any
from datetime import datetime
import requests

def attribute_flight(api_key: str, origin: str, destination: str, departure_date: datetime, return_date: datetime) -> Optional[Dict[str, Any]]:
    url = "https://partners.api.skyscanner.net/apiservices/v3/flights/indicative/search"
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    payload = {
        "query": {
            "market": "ES",
            "locale": "en-GB",
            "currency": "EUR",
            "queryLegs": [
                {
                    "originPlace": {"queryPlace": {"iata": origin}},
                    "destinationPlace": {"queryPlace": {"iata": destination}},
                    "fixedDate": {
                        "year": departure_date.year,
                        "month": departure_date.month,
                        "day": departure_date.day
                    }
                },
                {
                    "originPlace": {"queryPlace": {"iata": destination}},
                    "destinationPlace": {"queryPlace": {"iata": origin}},
                    "fixedDate": {
                        "year": return_date.year,
                        "month": return_date.month,
                        "day": return_date.day
                    }
                }
            ]
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        return None

    data = response.json()
    results = data.get("content", {}).get("results", {})
    quotes = results.get("quotes", {})
    carriers = results.get("carriers", {})
    places = results.get("places", {})

    if not quotes:
        return None

    # Find the quote with the lowest price
    cheapest_quote = min(quotes.values(), key=lambda q: float(q["minPrice"]["amount"]))

    def get_place_info(place_id):
        place = places.get(place_id, {})
        return {"name": place.get("name"), "iata": place.get("iata")}

    def get_carrier_info(carrier_id):
        carrier = carriers.get(carrier_id, {})
        return {
            "name": carrier.get("name"),
            "iata": carrier.get("iata"),
            "imageUrl": carrier.get("imageUrl")
        }

    def format_leg(leg, is_direct):
        return {
            "from": get_place_info(leg["originPlaceId"]),
            "to": get_place_info(leg["destinationPlaceId"]),
            "departure": leg["departureDateTime"],
            "carrier": get_carrier_info(leg["marketingCarrierId"]),
            "is_direct": is_direct
        }

    return {
        "price": float(cheapest_quote["minPrice"]["amount"]),
        "outbound": format_leg(cheapest_quote["outboundLeg"], cheapest_quote.get("isDirect", False)),
        "inbound": format_leg(cheapest_quote["inboundLeg"], cheapest_quote.get("isDirect", False))
    }



def save_to_json(data: Dict[str, Any], filename: str) -> None:
    """
    Save data to a JSON file
    
    Parameters:
    - data (dict): The data to save
    - filename (str): Name of the file to save to
    """
    # Create 'flight_data' directory if it doesn't exist
    os.makedirs('flight_data', exist_ok=True)
    
    # Full path for the file
    filepath = os.path.join('flight_data', filename)
    
    # Save the data
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def main() -> None:
    load_dotenv()
    
    # Access environment variables
    api_key = os.getenv("SKYSCANNER_API_KEY")
    
    # List of origin airports (IATA codes)
    origins = ["BCN", "MAD", "CDG", "FRA", "AMS", "FCO", "ZRH", "CPH", "DUB", "LIS"]

    # Shared travel details
    destination = "LHR"
    arrival_date = "2025-06-15"
    departure_date = "2025-06-20"

    for origin in origins:
        # Convert string dates to datetime objects
        arrival_date_obj = datetime.strptime(arrival_date, "%Y-%m-%d")
        departure_date_obj = datetime.strptime(departure_date, "%Y-%m-%d")

        # Fetch flight data for arrival
        flights_data = attribute_flight(api_key, origin, destination, arrival_date_obj, departure_date_obj)
        if flights_data:
            # Create filename with origin, destination and date
            flights_name = f"{origin}_to_{destination}.json"
            save_to_json(flights_data, flights_name)


if __name__ == "__main__":
    main()