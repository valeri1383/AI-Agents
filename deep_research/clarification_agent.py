from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = """You are a research assistant that helps clarify and refine research queries.
Given a research query, generate exactly 3 clarification questions that would help make the research 
more focused and comprehensive. These questions should cover different aspects like:
- Scope (time period, geographic region, specific industries/sectors)
- Focus (what specific aspects are most important)
- Context (what will this research be used for, target audience)
- Depth (technical level, specific metrics or outcomes of interest)

Make the questions specific and actionable. Avoid yes/no questions."""

class ClarificationQuestion(BaseModel):
    question: str = Field(description="A clarification question to refine the research")
    purpose: str = Field(description="Why this question helps improve the research")

class ClarificationQuestions(BaseModel):
    questions: list[ClarificationQuestion] = Field(description="List of 3 clarification questions")


clarification_agent = Agent(
    name="ClarificationAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ClarificationQuestions,
)

