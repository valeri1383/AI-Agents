from agents import Agent

def create_oppose_agent(motion):
    instructions = f"Present a clear argument against the motion: '{motion}'"
    return Agent(name="Oppose Agent", instructions=instructions, model="gpt-4o-mini")
