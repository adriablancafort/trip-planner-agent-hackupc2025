from typing import List
from models import SearchHotelRequest
from amadeus import Client
import os
import requests


def get_access_token(client_id, client_secret):
    """
    Obtain an access token from the Amadeus API.
    """
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    headers = { "Content-Type": "application/x-www-form-urlencoded" }
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status() 
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except ValueError:
        print("Error parsing the response JSON.")
    return None

def format_hotel_results(data):
    """
    Format hotel search results as a Markdown table.
    """
    if not data or 'data' not in data:
        return "No hotel data available."
    
    # Start building the markdown table
    md_table = "# Hotel Options\n\n"
    md_table += "| Hotel Name | Hotel Type | Chain Code | Price | Room Description |\n"
    md_table += "|------------|------------|------------|-------|------------------|\n"
    
    for hotel_data in data.get('data', []):
        hotel_type = hotel_data.get('hotel', {}).get('type', 'Unknown Type')
        hotel_name = hotel_data.get('hotel', {}).get('name', 'Unknown Hotel')
        chain_code = hotel_data.get('hotel', {}).get('chainCode', 'Unknown Chain')
            
        currency = hotel_data.get('offers', [{}])[0].get('price', {}).get('currency', 'Unknown Currency')
        price = hotel_data.get('offers', [{}])[0].get('price', {}).get('total', 'Unknown Price')

        description = hotel_data.get('offers', [{}])[0].get('room', {}).get('description', {}).get('text', 'Unknown Description')

        md_table += f"| {hotel_name} | {hotel_type} | {chain_code} | {price} {currency} | {description} |\n"
    
    return md_table


def get_hotel_list(client_id:str, client_secret:str, cityCode:str) -> List[str]:
    """ Get a list of hotel IDs for a given city code """
    amadeus = Client(
        client_id=client_id,
        client_secret=client_secret
    )
    response = amadeus.reference_data.locations.hotels.by_city.get(cityCode=cityCode)
    return [hotel['hotelId'] for hotel in response.data]


def search_hotels(params: SearchHotelRequest):
    """
    Search for hotels using the API.
    """
    client_id=os.getenv("AMADEUS_API_KEY")
    client_secret=os.getenv("AMADEUS_API_SECRET")

    hotelIds = get_hotel_list(client_id, client_secret, params.locationIata)[:15]

    access_token = get_access_token(client_id, client_secret)

    formated_date = f"{params.year}-{params.month}-{params.day}" if params.month > 9 else f"{params.year}-0{params.month}-{params.day}"

    url = 'https://test.api.amadeus.com/v3/shopping/hotel-offers'
    params = {
        'hotelIds': hotelIds,
        'adults': params.adults,
        'checkInDate': formated_date,
        'bestRateOnly': 'true',
        'currency': 'EUR'
    }
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    offers_response = requests.get(url, headers=headers, params=params)
    offers_response.raise_for_status()

    hotels = format_hotel_results(offers_response.json())
    print(hotels)
    return hotels
