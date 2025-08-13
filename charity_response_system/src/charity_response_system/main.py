#!/usr/bin/env python
import warnings
from datetime import datetime
from .crew import CharityResponseCrew
from dotenv import load_dotenv
import os


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

load_dotenv()

def run():
    """
    Run the Charity Response Crew.
    """

    print(f"SERPER_API_KEY loaded: {'Yes' if os.getenv('SERPER_API_KEY') else 'No'}")


    inputs = {
        'focus_area': 'Humanitarian Crises',
        'current_date': str(datetime.now())
    }

    # Create and run the crew
    result = CharityResponseCrew().crew().kickoff(inputs=inputs)

    # Print the result
    print("\n\n=== FINAL DECISION ===\n\n")
    print(result.raw)


if __name__ == "__main__":
    run()
