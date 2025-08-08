import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager

load_dotenv(override=True)

# Global state to store clarification questions and manager
research_state = {
    "manager": ResearchManager(),
    "current_query": None,
    "clarification_questions": None
}


async def start_research(query: str):
    """Start research and return clarification questions"""
    research_state["current_query"] = query
    research_state["manager"] = ResearchManager()

    async for chunk in research_state["manager"].run(query):
        if isinstance(chunk, dict) and chunk.get("type") == "clarification_questions":
            research_state["clarification_questions"] = chunk["questions"]
            return (
                "Please answer these clarification questions to refine your research:",
                gr.update(visible=True),
                gr.update(visible=True, value=research_state["clarification_questions"][0]),
                gr.update(visible=True),
                gr.update(visible=True, value=research_state["clarification_questions"][1]),
                gr.update(visible=True),
                gr.update(visible=True, value=research_state["clarification_questions"][2]),
                gr.update(visible=True),
                gr.update(visible=True)
            )
    return "Research started...", None, None, None, None, None, None, None, None


async def run_with_clarifications(q1_answer, q2_answer, q3_answer):
    """Run research with clarification answers"""
    if not research_state["clarification_questions"]:
        yield "No clarification questions found. Please start a new research."
        return

    clarifications = {
        research_state["clarification_questions"][0]: q1_answer,
        research_state["clarification_questions"][1]: q2_answer,
        research_state["clarification_questions"][2]: q3_answer,
    }

    async for chunk in research_state["manager"].run(
            research_state["current_query"],
            clarifications
    ):
        if isinstance(chunk, str):
            yield chunk


# Simple version without clarifications (fallback)
async def run_simple_research(query: str):
    """Run research without clarification questions"""
    research_state["current_query"] = query
    research_state["manager"] = ResearchManager()

    async for chunk in research_state["manager"].run(query):
        if isinstance(chunk, str):
            yield chunk


with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research with Optional Clarifications")

    with gr.Row():
        query_textbox = gr.Textbox(
            label="What topic would you like to research?",
            placeholder="Enter your research query...",
            scale=3
        )
        start_button = gr.Button("Start Research", variant="primary", scale=1)
        simple_button = gr.Button("Skip Clarifications", variant="secondary", scale=1)

    status = gr.Markdown(label="Status")

    # Clarification section (initially hidden)
    with gr.Column(visible=False) as clarification_section:
        gr.Markdown("### Clarification Questions")
        gr.Markdown("Please provide answers to help focus the research:")

        q1 = gr.Textbox(label="Question 1", visible=False, interactive=False)
        a1 = gr.Textbox(label="Your Answer 1", visible=False, placeholder="Enter your answer...")

        q2 = gr.Textbox(label="Question 2", visible=False, interactive=False)
        a2 = gr.Textbox(label="Your Answer 2", visible=False, placeholder="Enter your answer...")

        q3 = gr.Textbox(label="Question 3", visible=False, interactive=False)
        a3 = gr.Textbox(label="Your Answer 3", visible=False, placeholder="Enter your answer...")

        proceed_button = gr.Button("Proceed with Focused Research", variant="primary", visible=False)

    report = gr.Markdown(label="Research Report")

    # Event handlers
    start_button.click(
        fn=start_research,
        inputs=[query_textbox],
        outputs=[status, clarification_section, q1, a1, q2, a2, q3, a3, proceed_button]
    )

    proceed_button.click(
        fn=run_with_clarifications,
        inputs=[a1, a2, a3],
        outputs=[report]
    )

    # Simple research without clarifications
    simple_button.click(
        fn=run_simple_research,
        inputs=[query_textbox],
        outputs=[report]
    )

    # Allow Enter key to start research
    query_textbox.submit(
        fn=start_research,
        inputs=[query_textbox],
        outputs=[status, clarification_section, q1, a1, q2, a2, q3, a3, proceed_button]
    )

if __name__ == "__main__":
    ui.launch(inbrowser=True)