from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, RunContext, function_tool
from livekit.plugins import (
    openai,
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from skyscanner.flights import search_flights
from models import SearchFlightRequest

load_dotenv()


class TripPlannerAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""
            You are a helpful voice AI trip planner assistant. 
            Guide users through planning their trips by asking questions about:
            - Their origin location
            - Their destination
            - Their travel dates
            
            Use the search_flights tool to find flight options for them based on their answers.
            Explain the best flight options you find, including prices and airlines.
            If the user doesn't know airport codes, suggest some for major cities they mention.
            """
        )
    
    @function_tool()
    async def search_flights(self):
        """
        Search for flights using the Skyscanner API.
        
        Args:
            originIata: The origin airport code (IATA code, e.g., 'JFK')
            destinationIata: The destination airport code (IATA code, e.g., 'LAX')
            year: The year of travel (e.g., 2025)
            month: The month of travel (e.g., 8 for August)
        """
        params = SearchFlightRequest(
            originIata = "BCN",
            destinationIata = "JFK",
            year = 2025,
            month = 8
        )
        
        return search_flights(params)


async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()

    session = AgentSession(
        stt=deepgram.STT(model="nova-3", language="multi"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=cartesia.TTS(),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=TripPlannerAgent(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(), 
        ),
    )

    await session.generate_reply(
        instructions="Greet the user, introduce yourself as a trip planning assistant, and ask where they'd like to travel to."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))