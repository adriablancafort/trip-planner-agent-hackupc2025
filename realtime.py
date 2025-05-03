from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import openai, noise_cancellation
from models import FlightSearchParams
from skyscanner.flights import search_flights

load_dotenv()


class TripPlannerAgent(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful trip planner. Ask the user where they want to go, when, and from where. Then help them find flights.")

    async def on_message(self, message: str) -> str:
        if not hasattr(self, "stage"):
            self.stage = 0
            self.trip_info = {}

        if self.stage == 0:
            self.stage += 1
            return "Where would you like to travel to?"

        elif self.stage == 1:
            self.trip_info["destination"] = message.strip()
            self.stage += 1
            return "Great. Where will you be flying from?"

        elif self.stage == 2:
            self.trip_info["origin"] = message.strip()
            self.stage += 1
            return "And when do you plan to depart? Please say the date like year-month-day."

        elif self.stage == 3:
            self.trip_info["departure_date"] = message.strip()
            self.stage += 1
            return "Thanks! Let me find flights for you."

        elif self.stage == 4:
            # Fetch flights
            params = FlightSearchParams(
                origin=self.trip_info["origin"].upper(),
                destination=self.trip_info["destination"].upper(),
                departure_date=self.trip_info["departure_date"],
                market="US",
                locale="en-US",
                currency="USD"
            )
            result = search_flights(params)

            if not result["success"] or not result["flights"]:
                return "Sorry, I couldn't find any flights matching that. Please try again."

            top = result["flights"][:1][0]  # Just one result for now
            summary = (
                f"Here's a flight from {top['origin']} to {top['destination']} on {top.get('departure_date', 'your selected date')}, "
                f"with {top['carrier']} for {top['price']['amount']} {top['price']['currency']}."
            )
            self.stage += 1
            return summary + " Would you like to search for another destination?"

        else:
            self.stage = 0
            return "Okay, let's start over. Where would you like to go?"


async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()

    session = AgentSession(
        llm=openai.realtime.RealtimeModel(voice="coral")
    )

    await session.start(
        room=ctx.room,
        agent=TripPlannerAgent(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC()
        ),
    )

    await session.generate_reply("Hi! I can help you plan your next trip.")


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
