from pydantic_ai import AIModel

class TravelPlannerAgent(AIModel):
    """
    A simple AI agent for travel planning.
    """
    def plan_trip(self, destination: str, start_date: str, end_date: str):
        """
        Plan a trip to the specified destination within the given dates.
        """
        return f"Planning your trip to {destination} from {start_date} to {end_date}."

if __name__ == "__main__":
    agent = TravelPlannerAgent()
    print(agent.plan_trip("Paris", "2025-06-01", "2025-06-10"))