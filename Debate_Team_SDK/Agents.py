from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Agent:
    def __init__(self, name, instructions, motion, model):
        self.name = name
        self.instructions = instructions
        self.motion = motion
        self.model = model

    def run(self):
        # Use the new client to create chat completion
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.instructions}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    async def run_async(self):
        import asyncio
        return await asyncio.to_thread(self.run)
