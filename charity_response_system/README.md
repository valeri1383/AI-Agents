# Charity Response System

Welcome to the Charity Response System, powered by crewAI. This AI-driven humanitarian response platform automatically detects global crises, evaluates their urgency, finds relevant charities, and creates actionable response plans. Our goal is to enable rapid, coordinated humanitarian aid through intelligent multi-agent collaboration.

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses UV for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```
pip install uv
```

Next, navigate to your project directory and install the dependencies:

```
crewai install
```

## Customizing

**Add your API keys into the `.env` file:**
* `OPENAI_API_KEY` - Your OpenAI API key
* `SERPER_API_KEY` - Your Serper search API key (get free at serper.dev)
* `PUSHOVER_USER` - (Optional) Pushover user key for notifications
* `PUSHOVER_TOKEN` - (Optional) Pushover app token

* Modify `src/charity_response_system/config/agents.yaml` to define your humanitarian response agents
* Modify `src/charity_response_system/config/tasks.yaml` to customise crisis detection and response tasks
* Modify `src/charity_response_system/crew.py` to add your own tools and response logic
* Modify `src/charity_response_system/main.py` to customise crisis monitoring parameters

## Running the Project

To kickstart your humanitarian response crew and begin crisis monitoring, run this from the root folder of your project:

```
$ crewai run
```

This command initialises the Charity Response Crew, assembling specialised agents for crisis detection, impact assessment, charity vetting, and response planning as defined in your configuration.

This system will continuously scan for humanitarian crises and generate comprehensive reports in the `output/` folder, including:
* `events.md` - Detected humanitarian crises
* `assessment_report.md` - Crisis urgency analysis
* `selected_charities.md` - Vetted charity recommendations
* `action_plan.md` - Strategic response plans
* `decision_report.md` - Executive decisions and next steps

## Understanding Your Crew

The Charity Response Crew is composed of six specialised AI agents working in a hierarchical structure:

**Manager Agent** - Executive oversight and final decision-making
* **Event Watcher Agent** - Monitors global news and humanitarian databases for emerging crises
* **Impact Assessment Agent** - Evaluates crisis severity, urgency, and resource requirements
* **Charity Finder Agent** - Discovers relevant charitable organizations and NGOs
* **Charity Vetting Agent** - Verifies charity legitimacy, efficiency, and transparency
* **Action Planner Agent** - Creates comprehensive response strategies with timelines and budgets

These agents collaborate on crisis response tasks defined in `config/tasks.yaml`, leveraging web search, data analysis, and strategic planning to coordinate effective humanitarian aid. The `config/agents.yaml` file outlines each agent's specialised role in the crisis response pipeline.

## Features

* **Real-time Crisis Detection** - Automated monitoring of global humanitarian emergencies
* **Impact Assessment** - Data-driven urgency scoring and resource requirement analysis
* **Charity Verification** - Comprehensive vetting of charitable organizations
* **Strategic Planning** - Actionable response plans with budgets and timelines
* **Professional Reports** - Executive-ready markdown reports with tables and analysis
* **Push Notifications** - Real-time alerts for critical situations
