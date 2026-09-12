#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from review_crew.crew import ReviewCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run(pr_url: str, project_name: str, project_description: str):
    """
    Run the crew.
    """
    project_info = (
        f"Project name: {project_name}\n"
        f"Project description: {project_description}\n"
        f"Pull request URL: {pr_url}"
    )
    file_review_instructions = (
        "Use the codebase analysis to find files in your lane (and matching changed_files). "
        f"Read those files with github_client: action=get_file and pr_url={pr_url}. "
        "Do not review from filenames or the project description alone."
    )
    inputs = {
        'pr_url': pr_url,
        'project_name': project_name,
        'project_description': project_description,
        'project_info': project_info,
        'file_review_instructions': file_review_instructions,
        'specialist_expected_output': "A SpecialistReview Pydantic output. Use empty lists if there is nothing to report.",
        'current_year': str(datetime.now().year),
    }

    try:
        return ReviewCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": "",
        "current_year": ""
    }

    try:
        result = ReviewCrew().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
