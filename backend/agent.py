from livekit.agents import Agent, function_tool
from api.flights import search_flights
from api.hotels import search_hotels
from api.events import search_events
from api.email import send_email
from models import SearchFlightRequest, SearchHotelRequest, SearchEventRequest, SendEmail


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
            
            After providing flight, hotel, and event recommendations, ask the user if they would like to
            receive all the details by email. If they agree, collect their email address and use the send_email
            function to deliver a comprehensive trip summary including all recommended flights, accommodations and
            events discussed.
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
            locationIata: The city IATA code of the location for hotel search (e.g., 'BCN'). NOT THE AIRPORT IATA!
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

    @function_tool()
    async def send_email(self, email: str, subject: str, content: str):
        """
        Send email.
        
        Args:
            email: The email address to send the information. Make sure to get the correct address from the user.
            subject: The subject of the email
            content: The content of the email
        """
        params = SendEmail(
            email=email,
            subject=subject,
            content=content
        )
        
        return send_email(params)