from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from pydantic import BaseModel, Field
from crewai_tools import SerperDevTool
from .tools.push_tool import PushNotificationTool
import os
from dotenv import load_dotenv
from pathlib import Path


project_root = Path(__file__).parent.parent.parent
env_path = project_root / '.env'

load_dotenv(env_path)

print(f"Looking for .env at: {env_path}")
print(f".env file exists: {env_path.exists()}")
print(f"SERPER_API_KEY loaded: {os.getenv('SERPER_API_KEY')}")


load_dotenv(env_path)

# --- Pydantic Output Models ---
class CrisisEvent(BaseModel):
    """A verified crisis or disaster event that requires aid"""
    name: str = Field(description="Short descriptive title of the crisis")
    location: str = Field(description="Primary location affected")
    date: str = Field(description="Date the crisis occurred or was detected")
    summary: str = Field(description="Brief summary of the crisis")
    urgency_level: str = Field(description="Initial urgency assessment (High/Medium/Low)")
    source_links: List[str] = Field(description="List of verified source URLs")

class CrisisEventList(BaseModel):
    """List of multiple detected crisis events formatted for reporting"""
    events: List[CrisisEvent] = Field(description="List of crisis events detected")
    total_count: int = Field(description="Total number of crises found")
    report_summary: str = Field(description="Executive summary of all detected crises")

class UrgencyAssessment(BaseModel):
    """Severity and priority evaluation of a crisis"""
    event_title: str = Field(description="Title of the crisis being assessed")
    location: str = Field(description="Location of the crisis")
    urgency_score: int = Field(description="Urgency rating from 1–10")
    aid_type: str = Field(description="Primary type of aid needed (food, water, shelter, medical, other)")
    affected_population: str = Field(description="Estimated number of people affected")
    justification: str = Field(description="Detailed reason for the assigned urgency score")
    immediate_needs: List[str] = Field(description="List of immediate needs and requirements")

class UrgencyAssessmentList(BaseModel):
    """List of urgency assessments for crises with reporting structure"""
    assessments: List[UrgencyAssessment] = Field(description="List of crisis urgency evaluations")
    overall_risk_level: str = Field(description="Overall risk assessment (Critical/High/Medium/Low)")
    priority_ranking: List[str] = Field(description="List of crisis names ranked by priority")
    recommendations: str = Field(description="Strategic recommendations for response prioritization")

class Charity(BaseModel):
    """A vetted charity organization with detailed information"""
    name: str = Field(description="Name of the charity")
    focus_area: str = Field(description="Type of aid provided")
    region: str = Field(description="Region where it operates for this crisis")
    contact_info: str = Field(description="Contact information (website, email, phone)")
    specialization: str = Field(description="Specific areas of expertise")
    track_record: str = Field(description="Brief description of experience and achievements")
    efficiency_score: float = Field(description="Efficiency rating as a percentage")
    verification_notes: str = Field(description="Notes on legitimacy and operational capacity")
    trust_score: float = Field(description="Overall trust score as a percentage")

class CharityList(BaseModel):
    """List of vetted charities with comprehensive reporting"""
    charities: List[Charity] = Field(description="List of approved charities responding to the crisis")
    total_vetted: int = Field(description="Total number of charities that passed vetting")
    total_rejected: int = Field(description="Total number of charities rejected")
    top_recommendations: List[str] = Field(description="Names of top 3 recommended charities")
    vetting_criteria: str = Field(description="Summary of criteria used for evaluation")

class ActionItem(BaseModel):
    """Individual action item in the response plan"""
    action_type: str = Field(description="Type of action (donation, campaign, volunteer coordination, etc.)")
    target_crisis: str = Field(description="Which crisis this action addresses")
    responsible_charity: str = Field(description="Which charity will execute this action")
    timeline: str = Field(description="Expected timeframe for completion")
    budget: float = Field(description="Estimated budget required")
    expected_impact: str = Field(description="Projected outcomes and impact")
    success_metrics: List[str] = Field(description="How success will be measured")

class ActionPlan(BaseModel):
    """Comprehensive planned actions to respond to a crisis"""
    executive_summary: str = Field(description="High-level overview of the action plan")
    actions: List[ActionItem] = Field(description="List of specific actions to be taken")
    total_budget: float = Field(description="Total estimated budget for all actions")
    implementation_timeline: str = Field(description="Overall timeline for plan execution")
    risk_assessment: str = Field(description="Potential risks and mitigation strategies")
    monitoring_plan: str = Field(description="How progress will be tracked and reported")



# --- Crew Definition ---

@CrewBase
class CharityResponseCrew():
    """Charity Response System crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'


    @agent
    @agent
    def event_watcher_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['event_watcher_agent'],
            verbose=True,
            tools=[SerperDevTool()],
            # Add reporting instructions
            system_message="""You are a professional humanitarian crisis analyst. 
                Always format your outputs as comprehensive markdown reports with proper tables, 
                headers, and professional presentation. Use clear, concise language suitable 
                for emergency response stakeholders."""
        )

    @agent
    def impact_assessment_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['impact_assessment_agent'],
            verbose=True,
            tools=[SerperDevTool()],
            system_message="""You are a crisis severity analyst. Present your assessments 
                in professional markdown format with clear tables and structured analysis. 
                Focus on data-driven insights and actionable recommendations."""
        )

    @agent
    def charity_finder_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['charity_finder_agent'],
            verbose=True,
            tools=[SerperDevTool()],
            system_message="""You are a nonprofit sector specialist. Create detailed, 
                well-formatted reports about charitable organizations with comprehensive 
                tables and professional presentation suitable for decision-makers."""
        )

    @agent
    def charity_vetting_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['charity_vetting_agent'],
            verbose=True,
            tools=[SerperDevTool()],
            system_message="""You are a nonprofit verification expert. Present your 
                vetting results in clear, professional markdown format with detailed 
                tables and transparent evaluation criteria."""
        )

    @agent
    def action_planner_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['action_planner_agent'],
            verbose=True,
            tools=[PushNotificationTool()],
            system_message="""You are a humanitarian response strategist. Create 
                comprehensive, actionable plans presented in professional markdown format 
                with clear timelines, budgets, and implementation details."""
        )

    @agent
    def manager_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['manager_agent'],
            verbose=True,
            allow_delegation=True,
            memory=True,
            system_message="""You are the executive decision-maker for humanitarian 
                response operations. Present all decisions and approvals in executive-level 
                markdown reports suitable for board presentation and stakeholder communication."""
        )

    # Tasks remain the same but will now use the updated YAML configuration
    @task
    def event_watching(self) -> Task:
        return Task(
            config=self.tasks_config['event_watching'],
            output_pydantic=CrisisEventList,
        )

    @task
    def impact_assessment(self) -> Task:
        return Task(
            config=self.tasks_config['impact_assessment'],
            output_pydantic=UrgencyAssessmentList,
        )

    @task
    def charity_finding(self) -> Task:
        return Task(
            config=self.tasks_config['charity_finding'],
            output_pydantic=CharityList,
        )

    @task
    def charity_vetting(self) -> Task:
        return Task(
            config=self.tasks_config['charity_vetting'],
            output_pydantic=CharityList,
        )

    @task
    def action_planning(self) -> Task:
        return Task(
            config=self.tasks_config['action_planning'],
            output_pydantic=ActionPlan,
        )

    @task
    def decision_and_execution(self) -> Task:
        return Task(
            config=self.tasks_config['decision_and_execution'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CharityResponseSystem crew with enhanced reporting"""
        return Crew(
            agents=[
                self.event_watcher_agent(),
                self.impact_assessment_agent(),
                self.charity_finder_agent(),
                self.charity_vetting_agent(),
                self.action_planner_agent()
            ],
            tasks=self.tasks,
            verbose=True,
            process=Process.hierarchical,
            manager_agent=self.manager_agent()
        )