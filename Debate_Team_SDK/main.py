import asyncio
from Agents import Agent

motion = "Should AI should replace human teachers in the classroom?"
instructions1= f"Are you skilled debater. Present a short and clear argument in favor of the motion: '{motion}'"
instructions2= f"Are you skilled debater. Present a short and clear argument against of the motion: '{motion}'"
instructions3= f"Given the response from both debaters announce the winner in each round and the final winner in the end."
model="gpt-4o-mini"

propose_agent = Agent('propose agent', instructions1, motion, model)
oppose_agent = Agent('oppose agent', instructions2, motion, model)
judge_agent = Agent('judge agent', instructions3, motion, model)

async def debate_round(round_num):
    print(f"\n=== Round {round_num + 1} ===")
    agents = [judge_agent, propose_agent, oppose_agent]

    for agent in agents:
        result = agent.run()  # Call normal sync method
        print(f"{agent.name}: {result}")

async def main():
    rounds = 3
    for i in range(rounds):
        await debate_round(i)

if __name__ == "__main__":
    asyncio.run(main())