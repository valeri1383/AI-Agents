from agents import Runner, trace, gen_trace_id
from search_agent import search_agent
from clarification_agent import clarification_agent, ClarificationQuestions
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
from email_agent import email_agent
import asyncio


class ResearchManager:

    async def run(self, query: str, clarifications: dict = None):
        """ Run the enhanced research process with clarification questions"""
        trace_id = gen_trace_id()
        with trace("Enhanced Research trace", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"

            # Step 1: Generate clarification questions if no clarifications provided
            if not clarifications:
                yield "Generating clarification questions..."
                clarification_questions = await self.generate_clarifications(query)
                # Return questions to UI for user input
                yield {
                    "type": "clarification_questions",
                    "questions": [q.question for q in clarification_questions.questions]
                }
                return  # Wait for user to provide answers

            # Step 2: Plan searches based on clarifications
            yield "Planning targeted searches based on clarifications..."
            search_plan = await self.plan_searches_with_clarifications(query, clarifications)

            # Step 3: Perform searches
            yield "Executing targeted searches..."
            search_results = await self.perform_searches(search_plan)

            # Step 4: Write enhanced report
            yield "Writing comprehensive report..."
            report = await self.write_enhanced_report(query, clarifications, search_results)

            # Step 5: Send email
            yield "Sending detailed report via email..."
            await self.send_email(report)

            yield "Research complete - enhanced report generated!"
            yield report.markdown_report

    async def generate_clarifications(self, query: str) -> ClarificationQuestions:
        """ Generate clarification questions for the query """
        print("Generating clarification questions...")
        result = await Runner.run(
            clarification_agent,
            f"Research Query: {query}",
        )
        return result.final_output_as(ClarificationQuestions)

    async def plan_searches_with_clarifications(self, query: str, clarifications: dict) -> WebSearchPlan:
        """ Plan searches incorporating clarification answers """
        print("Planning enhanced searches...")

        # Format clarifications for the prompt
        clarification_text = "\n".join([
            f"Q: {question}\nA: {answer}"
            for question, answer in clarifications.items()
        ])

        enhanced_prompt = f"""
        Original Query: {query}

        Clarifications:
        {clarification_text}

        Please create targeted searches that incorporate these clarifications.
        """

        result = await Runner.run(
            planner_agent,
            enhanced_prompt,
        )

        print(f"Will perform {len(result.final_output.searches)} targeted searches")
        return result.final_output_as(WebSearchPlan)

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """ Same as original - perform the searches """
        print("Searching...")
        num_completed = 0
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            print(f"Searching... {num_completed}/{len(tasks)} completed")
        print("Finished searching")
        return results

    async def search(self, item: WebSearchItem) -> str | None:
        """ Same as original - perform individual search """
        input = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(search_agent, input)
            return str(result.final_output)
        except Exception:
            return None

    async def write_enhanced_report(self, query: str, clarifications: dict, search_results: list[str]) -> ReportData:
        """ Write report incorporating clarifications """
        print("Writing enhanced report...")

        clarification_summary = "\n".join([
            f"- {question}: {answer}"
            for question, answer in clarifications.items()
        ])

        enhanced_input = f"""
        Original Query: {query}

        Research Focus (based on clarifications):
        {clarification_summary}

        Research Findings:
        {search_results}

        Please write a comprehensive report that directly addresses the original query while 
        incorporating the specific focus areas identified in the clarifications.
        """

        result = await Runner.run(writer_agent, enhanced_input)
        print("Finished writing enhanced report")
        return result.final_output_as(ReportData)

    async def send_email(self, report: ReportData) -> None:
        """ Same as original - send email """
        print("Writing email...")
        await Runner.run(email_agent, report.markdown_report)
        print("Email sent")
        return report




