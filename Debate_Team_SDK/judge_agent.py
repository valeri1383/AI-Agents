from agents import Agent

def create_judge_agent(motion):
    instructions = f"Facilitate a structured debate on: '{motion}', ensuring equal speaking time."
    return Agent(name="Judge Agent", instructions=instructions, model="gpt-4o-mini")
