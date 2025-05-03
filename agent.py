from pydantic_ai import Agent, RunContext
from models import TripRequest, TripPlan, FlightSearchParams
from skyscanner.flights import search_flights

trip_planner = Agent(
    'openai:gpt-4o',
    deps_type=TripRequest,
    output_type=TripPlan,
    system_prompt="""
    You are a travel planning assistant. Help users plan trips by searching for flights 
    and providing recommendations. Use the search_flights_tool to find flight options.
    """
)

@trip_planner.tool
async def search_flights_tool(ctx: RunContext[TripRequest], params: FlightSearchParams) -> str:
    """Search for flights using the Skyscanner API"""
    results = search_flights(params)
    
    if not results["success"]:
        return f"Error searching for flights: {results['message']}"
    
    if not results["flights"]:
        return "No flights found matching your criteria."
    
    flight_options = [
        f"Option {i}: {flight['origin']} → {flight['destination']} "
        f"({'Direct' if flight['is_direct'] else 'Connecting'}) "
        f"with {flight['carrier']} "
        f"for {flight['price']['amount']} {flight['price']['currency']}"
        for i, flight in enumerate(results["flights"], 1)
    ]
    
    return f"Found {len(results['flights'])} flight options:\n\n" + "\n".join(flight_options)
