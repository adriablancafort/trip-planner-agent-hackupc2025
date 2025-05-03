from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()

agent = Agent(  
    'openai:gpt-4o',
    system_prompt='Be concise, reply with one sentence.',  
)

result = agent.run_sync('Where does "hello world" come from?')  
print(result.output)