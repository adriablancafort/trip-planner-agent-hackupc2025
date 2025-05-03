from dotenv import load_dotenv
from models import TripRequest, TripPlan
from agent import trip_planner
import json

load_dotenv()

def plan_trip(request: TripRequest) -> TripPlan:
    """Plan a trip based on the user's request"""
    prompt = f"Plan a trip from {request.origin}"
    if request.destination:
        prompt += f" to {request.destination}"
    if request.dates:
        prompt += f" on {request.dates}"
    if request.budget:
        prompt += f" with a budget of ${request.budget}"
    if request.preferences:
        prompt += f". Preferences: {request.preferences}"
    
    result = trip_planner.run_sync(prompt, deps=request)
    return result.output


if __name__ == "__main__":
    request = TripRequest(
        origin="Barcelona",
        destination="New York",
        dates="May 2025",
        budget=1000,
        preferences="I prefer direct flights and would like some cultural recommendations.",
        travelers=2
    )
    
    trip_plan = plan_trip(request)
    print(json.dumps(trip_plan.model_dump(), indent=2))
