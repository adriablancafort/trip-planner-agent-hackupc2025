import requests
from datetime import datetime, timedelta
from amadeus import Client, ResponseError
import random
from models import SearchEventRequest
TICKETMASTER_API_KEY = 'ld5c9Sc9ACkVQZU9GUuyuMor5Q4wvuC3'

def format_date(year: int, month: int, day: int) -> str:
    return f"{year:04d}-{month:02d}-{day:02d}"

def find_events_ticket_master(location:str, year:int, month:int, day:int):
    """
    Fetches events from Eventbrite, Ticketmaster, and Meetup based on location and date.

    Parameters:
    - location (str): The city or region to search events in.
    - date_str (str): The date in 'YYYY-MM-DD' format.

    Returns:
    - List of events with details.
    """
    events = []
    # Convert date string to datetime object

    try:
        date_obj = datetime.strptime(format_date(year,month,day), '%Y-%m-%d')
    except ValueError:
        print("Invalid date format. Please use 'YYYY-MM-DD'.")
        return events

    # Define date range: date ± 3 days
    start_date = date_obj.isoformat()
    end_date = (date_obj + timedelta(days=5)).isoformat()

    try:
        tm_url = 'https://app.ticketmaster.com/discovery/v2/events.json'
        tm_params = {
            'apikey': TICKETMASTER_API_KEY,
            'city': location,
            'startDateTime': f"{start_date}Z",
            'endDateTime': f"{end_date}Z"
        }
        tm_response = requests.get(tm_url, params=tm_params)
        if tm_response.status_code == 200:
            tm_data = tm_response.json()
            for event in tm_data.get('_embedded', {}).get('events', []):
                events.append({
                    'name': event['name'],
                    'start': event['dates']['start'].get('dateTime', ''),
                    'venue': event['_embedded']['venues'][0]['name'],
                    'url': event['url'],
                    'source': 'Ticketmaster'
                })
        else:
            print(f"Ticketmaster API error: {tm_response.status_code}")
    except Exception as e:
        print(f"Error fetching Ticketmaster events: {e}")
    all_events = []
    if len(events) < 20:
        all_events = events
    else: 
        all_events = random.sample(events, 20)
    lines = []
    for event in all_events:
        lines.append(f"| {event['venue']} | {event['name']} | {event['start']}")

    return lines


def find_events_amadeus(location: str, year: int, month: int, day: int):
    """
    Finds events near a given location starting from a specific date
    and over the following 4 days using the Amadeus API.

    Args:
        location (str): The name of the city or place.
        year (int): Start year.
        month (int): Start month.
        day (int): Start day.

    Returns:
        List of events (or empty list if none or error).
    """
    amadeus = Client(
        client_id='ronJiNRRBKMcYrCeXb4cW8D9D4W6qk2U',
        client_secret='Qt60LJ3Spm7lZUAA'
    )

    try:
        # Step 1: Get coordinates of the location
        location_response = amadeus.reference_data.locations.get(
            keyword=location,
            subType='CITY'
        )
        if not location_response.data:
            print(f"No location found for '{location}'")
            return []

        geo = location_response.data[0]['geoCode']
        latitude = geo['latitude']
        longitude = geo['longitude']

        # Step 2: Format dates
        start_date = datetime(year, month, day)
        end_date = start_date + timedelta(days=4)
        start_str = format_date(year, month, day)
        end_str = end_date.strftime('%Y-%m-%d')

        # Step 3: Search for events
        event_response = amadeus.shopping.activities.get(
            latitude=latitude,
            longitude=longitude,
            radius=10,  # km
            startDate=start_str,
            endDate=end_str
        )
        all_events = []
        if len(event_response.data) < 20:
            all_events = event_response.data
        else: 
            all_events = random.sample(event_response.data, 20)
        
        lines = []
        for event in all_events:
            lines.append(f"| {event['id']} | {event['name']} | {start_str}")

        return lines

    except ResponseError as e:
        print(f"Amadeus API error: {e}")
        return []
    

def search_events(params: SearchEventRequest):
    lines = []
    lines.append("## Event Options")
    lines.append("| Venue | description | Date |")
    lines.append("|-----------|-------|------|")
    lines = lines + find_events_amadeus(params.location, params.year,params.month,params.day)
    lines = lines + find_events_ticket_master(params.location, params.year,params.month,params.day)

    return "\n".join(lines)
    
