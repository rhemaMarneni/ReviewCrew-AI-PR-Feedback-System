import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from review_crew.services.github_client_service import GithubClientTool
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class ReviewCrew():
    """ReviewCrew crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def frontend_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_reviewer'],
            verbose=True
        )

    @agent
    def backend_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_reviewer'],
            verbose=True
        )

    @agent
    def security_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['security_reviewer'],
            verbose=True
        )

    @agent
    def test_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['test_reviewer'],
            verbose=True
        )

    @agent
    def lead_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_reviewer'],
            verbose=True,
        )

    @agent
    def codebase_analyzer(self) -> Agent:
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            raise ValueError("GITHUB_TOKEN is not set. Add it to review_crew/.env")
        return Agent(
            config=self.agents_config['codebase_analyzer'],
            verbose=True,
            tools=[GithubClientTool(token=token)]
        )

    @agent
    def review_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['review_manager'],
            verbose=True
        )

    @task
    def frontend_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_review_task'],
            verbose=True,
            output_file='output/frontend_review.md',
        )

    @task
    def backend_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['backend_review_task'],
            verbose=True,
            output_file='output/backend_review.md'
        )

    @task
    def security_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['security_review_task'],
            verbose=True,
            output_file='output/security_review.md'
        )

    @task
    def test_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['test_review_task'],
            verbose=True,
            output_file='output/test_review.md'
        )

    @task
    def lead_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['lead_review_task'],
            verbose=True,
            output_file='output/lead_review.md',
            output_pydantic=LeadReviewReport
        )

    @task
    def codebase_analyzer_task(self) -> Task:
        return Task(
            config=self.tasks_config['codebase_analyzer_task'],
            verbose=True,
        )

    @task
    def review_manager_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_manager_task'],
            verbose=True,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ReviewCrew crew"""

        manager = self.review_manager()
        specialists = [
            agent for agent in self.agents if getattr(agent, "role", None) != manager.role
        ]
        return Crew(
            agents=specialists,
            tasks=self.tasks,
            verbose=True,
            process=Process.hierarchical,
            manager_agent=manager,
        )
