import requests
import os
from typing import Dict, Any
from dotenv import load_dotenv
from models import FlightSearchParams

load_dotenv()


def search_flights(params: FlightSearchParams) -> Dict[str, Any]:
    """
    Search for flights using Skyscanner API based on provided parameters.

    Args:
        params: FlightSearchParams object with search criteria

    Returns:
        Dict: Flight search results with formatted flight options
    """
    api_key = os.environ.get("SKYSCANNER_API_KEY")
    
    if not api_key:
        return {"success": False, "message": "No API key provided", "flights": []}

    # API endpoint and headers
    url = "https://partners.api.skyscanner.net/apiservices/v3/flights/indicative/search"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    # Build query leg
    query_leg = {
        "originPlace": {"queryPlace": {"iata": params.origin}},
        "destinationPlace": {"queryPlace": {"iata": params.destination}}
    }
    
    # Handle date logic
    if params.departure_date:
        date_parts = params.departure_date.split("-")
        query_leg["fixedDate"] = {
            "year": int(date_parts[0]),
            "month": int(date_parts[1]),
            "day": int(date_parts[2])
        }
    else:
        query_leg["anytime"] = True

    # Request payload
    payload = {
        "query": {
            "market": params.market,
            "locale": params.locale,
            "currency": params.currency,
            "queryLegs": [query_leg]
        }
    }

    print(payload)
    try:
        # Make the request and process response
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Process the response to extract flight options
        flights = []
        if "content" in data and "results" in data["content"] and "quotes" in data["content"]["results"]:
            quotes = data["content"]["results"]["quotes"]
            carriers = data["content"]["results"].get("carriers", {})
            places = data["content"]["results"].get("places", {})
            
            for quote_id, quote in quotes.items():
                price = quote.get("minPrice", {}).get("amount", "0")
                is_direct = quote.get("isDirect", False)
                
                # Get leg details
                outbound = quote.get("outboundLeg", {})
                carrier_id = outbound.get("marketingCarrierId", "")
                carrier_name = carriers.get(carrier_id, {}).get("name", "Unknown")
                
                # Format the flight option
                flight = {
                    "price": {"amount": price, "currency": params.currency},
                    "is_direct": is_direct,
                    "carrier": carrier_name,
                    "origin": params.origin,
                    "destination": params.destination
                }
                
                # Add date info if available
                if "departureDateTime" in outbound:
                    dt = outbound["departureDateTime"]
                    if "year" in dt and dt["year"] > 0:
                        flight["departure_date"] = f"{dt['year']}-{dt['month']:02d}-{dt['day']:02d}"
                
                flights.append(flight)
        
        return {
            "success": True,
            "message": f"Found {len(flights)} flight options",
            "flights": flights
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "flights": []
        }
