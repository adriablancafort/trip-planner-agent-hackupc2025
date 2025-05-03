from pydantic_ai import Agent, RunContext
from models import TripRequest, TripPlan, FlightSearchParams, CarHireSearchParams
from skyscanner.flights import search_flights
from skyscanner.carhire import search_car_hire

trip_planner = Agent(
    'openai:gpt-4o',
    deps_type=TripRequest,
    output_type=TripPlan,
    system_prompt="""
    You are a travel planning assistant. Help users plan trips by searching for flights,
    car hire options, and providing recommendations. Use the search_flights_tool to find 
    flight options and the search_car_hire_tool to find car rental options when needed.
    """
)

@trip_planner.tool
async def search_flights_tool(ctx: RunContext[TripRequest], params: FlightSearchParams) -> str:
    """Search for flights using the Skyscanner API"""
    print(f"search flights tool called with params: {params}")
    results = search_flights(params)
    
    if not results["success"]:
        print("flight search error:", results["message"])
        return f"Error searching for flights: {results['message']}"
    
    if not results["flights"]:
        print("no flights found")
        return "No flights found matching your criteria."
    
    print(f"found {len(results['flights'])} flight options")
    flight_options = [
        f"Option {i}: {flight['origin']} → {flight['destination']} "
        f"({'Direct' if flight['is_direct'] else 'Connecting'}) "
        f"with {flight['carrier']} "
        f"for {flight['price']['amount']} {flight['price']['currency']}"
        for i, flight in enumerate(results["flights"], 1)
    ]
    
    return f"Found {len(results['flights'])} flight options:\n\n" + "\n".join(flight_options)

@trip_planner.tool
async def search_car_hire_tool(ctx: RunContext[TripRequest], params: CarHireSearchParams) -> str:
    """Search for car hire options using the Skyscanner API"""
    print(f"search car hire tool called with params: {params}")
    results = search_car_hire(params)
    
    if not results["success"]:
        print("car hire search error:", results["message"])
        return f"Error searching for car hire: {results['message']}"
    
    if not results["cars"]:
        print("no car hire options found")
        return "No car hire options found matching your criteria."
    
    print(f"found {len(results['cars'])} car hire options")
    car_options = [
        f"Option {i}: {car['vehicle_name']} ({car['vehicle_type']}) "
        f"for {car['price']['amount']} {car['price']['currency']} "
        f"from {car['pickup_date']} to {car['dropoff_date']}"
        for i, car in enumerate(results["cars"], 1)
    ]
    
    return f"Found {len(results['cars'])} car hire options:\n\n" + "\n".join(car_options)
