from livekit.agents import Agent, function_tool
from api.flights import search_flights
from api.hotels import search_hotels
from api.events import search_events
from models import SearchFlightRequest, SearchHotelRequest, SearchEventRequest


class TripPlannerAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""
            You are TripMates, a helpful AI team trip planner assistant.
            You are helping a group of friends who live in different locations and want to meet in the perfect destination.
            Your challenge is to design a smart travel plan that helps a group of friends easily discover the best destination based on their interests/preferences. 
            The focus is on creating a fun, collaborative experience where everyone has a say in the final decision.
            - Their origin location
            - Their destination
            - Their travel dates
            
            Use the search_flights tool to find flight options for them based on their answers.
            Use the search_hotels tool to find hotel options for them based on their answers.
            Use the search_events tool to find events.
            Explain the best flight options you find, including prices and airlines.
            The user will provide city names and you will have to use their IATA codes to search for flights.
            """
        )
    
    @function_tool()
    async def search_flights(self, originIata: str, destinationIata: str, month: int, day: int):
        """
        Search for flights using the Skyscanner API.
        
        Args:
            originIata: The origin airport code (IATA code, e.g., 'JFK')
            destinationIata: The destination airport code (IATA code, e.g., 'LAX')
            month: The month of travel (e.g., 8 for August)
            day: The day of travel (e.g., 15 for the 15th)
        """
        params = SearchFlightRequest(
            originIata=originIata,
            destinationIata=destinationIata,
            year=2025,
            month=month,
            day=day,
            market = "ES",
            locale = "es-ES",
            currency = "EUR"
        )
        
        return search_flights(params)
    
    @function_tool()
    async def search_hotels(self, locationIata: str, adults: int, month: int, day: int):
        """
        Search for hotels using the Amadeus API.
        
        Args:
            locationIata: The city IATA code of the location for hotel search (e.g., 'BCN')
            adults: The number of adults that will stay in the hotel
            month: The month of travel (e.g., 8 for August)
            day: The day of travel (e.g., 15 for the 15th)
        """
        params = SearchHotelRequest(
            locationIata=locationIata,
            adults=adults,
            year=2025,
            month=month,
            day=day,
        )
        
        return search_hotels(params)

    @function_tool()
    async def search_events(self, location: str, month: int, day: int):
        """
        Search for events using the Ticketmaster, Meetup, Amadeus APIs.
        
        Args:
            location: The location for event search (e.g., 'Barcelona')
            month: The month of travel (e.g., 8 for August)
            day: The day of travel (e.g., 15 for the 15th)
        """
        params = SearchEventRequest(
            location=location,
            year=2025,
            month=month,
            day=day,
        )
        
        return search_events(params)
