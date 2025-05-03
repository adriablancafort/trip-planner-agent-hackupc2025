from livekit.agents import Agent, function_tool
from skyscanner.flights import search_flights
from models import SearchFlightRequest


class TripPlannerAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""
            You are a helpful voice AI trip planner assistant. Be concise and direct.
            You are helping a group of friends who live in different locations and want to meet in the perfect destination.
            Your challenge is to design a smart travel plan that helps a group of friends easily discover the best destination based on their interests/preferences. 
            The focus is on creating a fun, collaborative experience where everyone has a say in the final decision.
            - Their origin location
            - Their destination
            - Their travel dates
            
            Use the search_flights tool to find flight options for them based on their answers.
            Explain the best flight options you find, including prices and airlines.
            If the user doesn't know airport codes, suggest some for major cities they mention.
            """
        )
    
    @function_tool()
    async def search_flights(self, originIata: str, destinationIata: str, month: int, day: int):
        """
        Search for flights using the Skyscanner API.
        
        Args:
            originIata: The origin airport code (IATA code, e.g., 'JFK')
            destinationIata: The destination airport code (IATA code, e.g., 'LAX')
            year: The year of travel (e.g., 2025)
            month: The month of travel (e.g., 8 for August)
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
