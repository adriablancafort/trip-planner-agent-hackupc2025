import requests
import os
from typing import Dict, Any
from dotenv import load_dotenv
from models import CarHireSearchParams
import pandas as pd

load_dotenv()


def get_entity_id(location: str) -> str:

    csv = pd.read_csv("data/iata_airports_and_locations_with_vibes.csv", header=0)
    id = location

    try:
        id = csv.loc[csv["IATA"] == location, "id"].values[0]
    
    except IndexError:
        print(f"IATA code {location} not found in CSV file. \
              Proceeding with default ID.")
        
    return id


def search_car_hire(params: CarHireSearchParams) -> Dict[str, Any]:
    """
    Search for car hire options using Skyscanner API based on provided parameters.

    Args:
        params: CarHireSearchParams object with search criteria

    Returns:
        Dict: Car hire search results with formatted options
    """
    api_key = os.environ.get("SKYSCANNER_API_KEY")
    
    if not api_key:
        return {"success": False, "message": "No API key provided", "cars": []}

    # API endpoint and headers
    url = "https://partners.api.skyscanner.net/apiservices/v1/carhire/indicative/search"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    # Get the entity ID for the location
    entity_id = get_entity_id(params.location_id)

    # Request payload
    payload = {
        "query": {
            "market": params.market,
            "locale": params.locale,
            "currency": params.currency,
            "pickUpDate": {
                "year": params.pickup_year,
                "month": params.pickup_month,
                "day": params.pickup_day
            },
            "dropOffDate": {
                "year": params.dropoff_year,
                "month": params.dropoff_month,
                "day": params.dropoff_day
            },
            "dateTimeGroupingType": "DATE_TIME_GROUPING_TYPE_BY_WEEK",
            "pickUpDropOffLocationEntityId": entity_id
        }
    }

    print(payload)
    try:
        # Make the request and process response
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Process the response to extract car hire options
        cars = []
        if "content" in data and "results" in data["content"] and "quotes" in data["content"]["results"]:
            quotes = data["content"]["results"]["quotes"]
            
            for quote_id, quote in quotes.items():
                price = quote.get("minPrice", {}).get("amount", "0")
                vehicle_info = quote.get("vehicleInfo", {})
                vehicle_name = vehicle_info.get("name", "Unknown vehicle")
                vehicle_type = vehicle_info.get("vehicleType", "Unknown type")
                
                # Format the car hire option
                car = {
                    "price": {"amount": price, "currency": params.currency},
                    "vehicle_name": vehicle_name,
                    "vehicle_type": vehicle_type,
                    "location": params.location_id,
                    "pickup_date": f"{params.pickup_year}-{params.pickup_month:02d}-{params.pickup_day:02d}",
                    "dropoff_date": f"{params.dropoff_year}-{params.dropoff_month:02d}-{params.dropoff_day:02d}"
                }
                
                cars.append(car)
        
        return {
            "success": True,
            "message": f"Found {len(cars)} car hire options",
            "cars": cars
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "cars": []
        }
