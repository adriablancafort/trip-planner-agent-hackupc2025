import json
import os
from typing import Any, Dict, Optional, TypedDict, Literal
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests

# Type definitions
class PlaceInfo(TypedDict):
    name: str
    iata: str

class CarrierInfo(TypedDict):
    name: str
    iata: str
    imageUrl: str

class FlightLeg(TypedDict):
    from_: PlaceInfo
    to: PlaceInfo
    departure: str
    carrier: CarrierInfo
    is_direct: bool

class FlightData(TypedDict):
    price: float
    outbound: FlightLeg
    inbound: FlightLeg


def find_cheapest_flight(
    api_key: str, 
    origin: str, 
    destination: str, 
    outbound_date: datetime, 
    return_date: datetime
) -> Optional[FlightData]:
    """
    Find the cheapest flight between two airports for specified dates.
    
    Args:
        api_key: Skyscanner API key
        origin: Origin airport IATA code
        destination: Destination airport IATA code
        outbound_date: Departure date from origin
        return_date: Return date from destination
        
    Returns:
        Flight data for cheapest route or None if no flights found
    """
    url = "https://partners.api.skyscanner.net/apiservices/v3/flights/indicative/search"
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    
    # Create request payload
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
                        "year": outbound_date.year,
                        "month": outbound_date.month,
                        "day": outbound_date.day
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

    # Make API request
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        return None

    # Extract relevant data
    data = response.json()
    results = data.get("content", {}).get("results", {})
    quotes = results.get("quotes", {})
    carriers = results.get("carriers", {})
    places = results.get("places", {})

    if not quotes:
        return None

    # Find the quote with the lowest price
    cheapest_quote = min(quotes.values(), key=lambda q: float(q["minPrice"]["amount"]))
    
    # Helper functions for data extraction
    def get_place_info(place_id: str) -> PlaceInfo:
        place = places.get(place_id, {})
        return PlaceInfo(name=place.get("name", ""), iata=place.get("iata", ""))

    def get_carrier_info(carrier_id: str) -> CarrierInfo:
        carrier = carriers.get(carrier_id, {})
        return CarrierInfo(
            name=carrier.get("name", ""),
            iata=carrier.get("iata", ""),
            imageUrl=carrier.get("imageUrl", "")
        )

    def format_leg(leg: Dict[str, Any], is_direct: bool) -> FlightLeg:
        return FlightLeg(
            from_=get_place_info(leg["originPlaceId"]),
            to=get_place_info(leg["destinationPlaceId"]),
            departure=leg["departureDateTime"],
            carrier=get_carrier_info(leg["marketingCarrierId"]),
            is_direct=is_direct
        )

    # Return formatted flight data
    return FlightData(
        price=float(cheapest_quote["minPrice"]["amount"]),
        outbound=format_leg(cheapest_quote["outboundLeg"], cheapest_quote.get("isDirect", False)),
        inbound=format_leg(cheapest_quote["inboundLeg"], cheapest_quote.get("isDirect", False))
    )


def save_to_json(data: Dict[str, Any], filename: str) -> None:
    """
    Save data to a JSON file
    
    Args:
        data: The data to save
        filename: Name of the file to save to
    """
    os.makedirs('flight_data', exist_ok=True)
    filepath = os.path.join('flight_data', filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def main() -> None:
    """Find and save cheapest flights to London from various European airports."""
    load_dotenv()
    api_key = os.getenv("SKYSCANNER_API_KEY")
    if not api_key:
        print("Error: SKYSCANNER_API_KEY environment variable not found")
        return
    
    # List of origin airports (IATA codes)
    origins = ["BCN", "MAD", "CDG", "FRA", "AMS", "FCO", "ZRH", "CPH", "DUB", "LIS"]
    destination = "LHR"
    
    # Date format: YYYY-MM-DD
    outbound_date_str = "2025-06-15"
    return_date_str = "2025-06-30"
    
    # Parse dates once
    original_outbound_date = datetime.strptime(outbound_date_str, "%Y-%m-%d")
    original_return_date = datetime.strptime(return_date_str, "%Y-%m-%d")

    for origin in origins:
        print(f"Searching flights from {origin} to {destination}...")
        
        # Initialize dates for this search
        outbound_date = original_outbound_date
        return_date = original_return_date
        
        # Set maximum attempts to avoid excessive API calls
        max_attempts = 10
        attempts = 0
        flight_data = None
        
        # Keep trying until flight data is found or max attempts reached
        while flight_data is None and attempts < max_attempts:
            print(f"  Attempt {attempts+1}: Searching with dates {outbound_date.strftime('%Y-%m-%d')} to {return_date.strftime('%Y-%m-%d')}...")
            flight_data = find_cheapest_flight(api_key, origin, destination, outbound_date, return_date)
            
            if flight_data is None:
                # Adjust dates for next attempt
                if attempts % 2 == 0:
                    # On even attempts, decrement outbound date
                    outbound_date = outbound_date - timedelta(days=1)
                else:
                    # On odd attempts, decrement return date
                    return_date = return_date + timedelta(days=1)
                     
            attempts += 1
        
        # Save flight data if found
        if flight_data:
            filename = f"{origin}_to_{destination}.json"
            save_to_json(flight_data, filename)
            print(f"SUCCESS: Flight data saved to {filename}")
            print(f"  Found flight with dates: {outbound_date.strftime('%Y-%m-%d')} to {return_date.strftime('%Y-%m-%d')}")
        else:
            print(f"FAILED: No flights found for {origin} to {destination} after {attempts} attempts")


if __name__ == "__main__":
    main()
